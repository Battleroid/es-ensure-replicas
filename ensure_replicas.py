import logging
import click
from functools import partial
from getpass import getuser
from elasticsearch import Elasticsearch

es_log = logging.getLogger('elasticsearch')
es_log.setLevel(logging.ERROR)

echo_err = partial(click.secho, err=True, fg='red')
echo_good = partial(click.secho, err=True, fg='green')


@click.command()
@click.argument('CLUSTER')
@click.argument('NODE')
@click.option(
    '--show-all',
    default=False,
    is_flag=True,
    help='Show all indexes replica settings')
@click.option(
    '--replicas',
    default=1,
    type=int,
    show_default=True,
    help='Replicas to set for indexes on node')
@click.option(
    '--username',
    default=getuser(),
    show_default=True,
    help='User for http auth')
@click.option(
    '--dump',
    default=None,
    type=click.Path(writable=True, dir_okay=False),
    help='Dump index list to file')
@click.password_option(confirmation_prompt=False, help='HTTP auth password')
def ensure(cluster, node, show_all, replicas, username, password, dump):

    # setup client
    if 'http' not in cluster:
        cluster = 'http://' + cluster
    ssl = 'https' in cluster

    es = Elasticsearch(
        cluster, use_ssl=ssl, verify_certs=ssl, http_auth=(username, password))

    # check if node is in listing
    all_nodes = [
        _['name']
        for _ in es.cat.nodes(
            filter_path='name', format='json', request_timeout=60)
    ]
    if node not in all_nodes:
        echo_err(f'{node} is not in node list')
        click.echo('Valid node names include:', err=True)
        for known_node in sorted(all_nodes):
            click.echo(f'  - {known_node}', err=True)
        raise click.Abort

    # get shards for that given node
    indexes = {
        _['index']
        for _ in es.cat.shards(
            filter_path='index,node', format='json', request_timeout=60)
        if _['node'] == node
    }

    try:
        indexes_settings = {
            index: int(v['settings']['index']['number_of_replicas'])
            for index, v in es.indices.get_settings(
                ','.join(indexes), filter_path='**.number_of_replicas')
            .items()
        }
    except:
        echo_err('Error submitting single URI for settings, '
                 'trying individual requests')
        indexes_settings = dict()
        for index in indexes:
            settings = es.indices.get_settings(
                index, filter_path='**.number_of_replicas')
            indexes_settings[index] = int(
                settings[index]['settings']['index']['number_of_replicas'])

    # is it all the same? all the same as what we're setting?
    indexes_settings_set = set(indexes_settings.values())
    if len(indexes_settings_set) == 1:
        indexes_settings_set.discard(replicas)
        if not indexes_settings_set:
            echo_good('Nothing to do; all indexes are already '
                      f'set to current replica count of "{replicas}"')
            raise click.Abort

    if not indexes:
        echo_err(f'No indexes on {node}')
        raise click.Abort

    # dump
    if dump:
        click.secho(f'Dumping index list for {node} to "{dump}"')
        with open(dump, 'w') as f:
            f.write('\n'.join(indexes))

    # list all the indexes that will be bumped
    to_be_changed = []
    already_set = []
    needed_indexes = []
    for index in sorted(indexes):
        msg = f'  - {index} '
        if indexes_settings[index] != replicas:
            msg += f'(from "{indexes_settings[index]}" to "{replicas}")'
            to_be_changed.append(click.style(msg, fg='yellow'))
            needed_indexes.append(index)
        else:
            msg += f'(already set to "{replicas}")'
            already_set.append(click.style(msg, fg='green'))

    click.secho(
        f'{len(to_be_changed)}/{len(indexes)} indexes will need to be changed. ',
        nl=False)
    click.secho('The following changes will be made', nl=False)
    click.secho(f' (showing all):\n' if show_all else ':\n')
    item_lists = (to_be_changed,
                  already_set) if show_all else (to_be_changed, )
    for item in item_lists:
        click.secho('\n'.join(item))

    click.confirm(
        f'\nAre you sure want to adjust the replicas to "{replicas}"?',
        abort=True,
        show_default=True,
        default=False)

    # adjust them
    payload = {'index.number_of_replicas': replicas}
    try:
        es.indices.put_settings(
            body=payload, index=','.join(needed_indexes), request_timeout=60)
    except:
        echo_err('Trying individual requests for settings')
        with click.progressbar(needed_indexes) as bar:
            for index in bar:
                es.indices.put_settings(
                    body=payload, index=index, request_timeout=60)


if __name__ == '__main__':
    ensure()
