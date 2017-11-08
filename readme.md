# es-ensure-replicas

Ensure all the indexes that reside on a given node actually have a specific number of replicas. Useful if you need to bump replicas up for a set of indexes that only reside on a node.

It will abort if there are no changes to be made to the indexes on the given node.

## Usage

```bash
$ ensure-replicas https://es-example.com:9200 data_node1 --replicas 0
Password:
The following changes will be made:
  - elasticsearch-2017.10.09-000053 (from "1" to "0")
  - elasticsearch-2017.10.10-000054 (from "1" to "0")
  - elasticsearch-2017.10.11-000055 (from "1" to "0")
  - elasticsearch-2017.10.12-000056 (from "1" to "0")
  - elasticsearch-2017.10.13-000057 (from "1" to "0")
  - elasticsearch-2017.10.14-000058 (from "1" to "0")
  - elasticsearch-2017.10.16-000059 (from "1" to "0")
  - elasticsearch-2017.10.17-000060 (from "1" to "0")
  - elasticsearch-2017.10.17-000061 (from "1" to "0")
  - elasticsearch-2017.10.18-000062 (from "1" to "0")
  - elasticsearch-2017.10.19-000063 (from "1" to "0")
  - elasticsearch-2017.10.20-000064 (from "1" to "0")
  - elasticsearch-2017.10.22-000065 (from "1" to "0")
  - elasticsearch-2017.10.23-000066 (from "1" to "0")
  - elasticsearch-2017.10.25-000067 (from "1" to "0")
  - elasticsearch-2017.10.26-000068 (from "1" to "0")
  - elasticsearch-2017.10.26-000069 (from "1" to "0")
  - filebeat-2017.10.08-000083 (from "1" to "0")
  - filebeat-2017.10.10-000084 (from "1" to "0")
  - filebeat-2017.10.11-000085 (from "1" to "0")
  - filebeat-2017.10.12-000086 (from "1" to "0")
  - filebeat-2017.10.14-000087 (from "1" to "0")
  - filebeat-2017.10.16-000088 (from "1" to "0")
  - filebeat-2017.10.18-000089 (from "1" to "0")
  - filebeat-2017.10.20-000090 (from "1" to "0")
  - filebeat-2017.10.21-000091 (from "1" to "0")
  - filebeat-2017.10.23-000092 (from "1" to "0")
  - filebeat-2017.10.25-000093 (from "1" to "0")

Are you sure want to adjust the replicas to "0"? [y/N]:
```

By default it will only display indexes that will be changed. Add the flag `--show-all` to show all indexes.
