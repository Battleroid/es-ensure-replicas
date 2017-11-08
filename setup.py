from setuptools import find_packages, setup
from pip.req import parse_requirements
from pip.download import PipSession

reqs = parse_requirements('requirements.txt', session=PipSession())
requirements = [str(req.req) for req in reqs]

setup(
    name='es-ensure-replicas',
    author='Casey Weed',
    author_email='casey@caseyweed.com',
    description='Adjust replicas for indexes on a node',
    url='https://github.com/battleroid/es-ensure-replicas',
    py_modules=['ensure_replicas'],
    install_requires=requirements,
    entry_points="""
        [console_scripts]
        ensure-replicas=ensure_replicas:ensure
    """
)
