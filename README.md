## Semantic Annotation

[![Docker Build](https://github.com/celluloid-camp/semantic-annotation/actions/workflows/docker-build.yml/badge.svg?event=push)](https://github.com/celluloid-camp/semantic-annotation/actions/workflows/docker-build.yml)
## Restore Neo4j database

First test if the neo4j is ready and `espectateur` database doesn't exists:

```bash
    docker exec --interactive --tty sematic-annotation-neo4j cypher-shell -u  neo4j  -p espectateurneo4j "SHOW DATABASES"
```

Restore the database with : 

```bash
    docker exec --interactive --tty sematic-annotation-neo4j neo4j-admin load --from=/dump/espectateur.dump  --database espectateur
```


Create the database after the load operation finishes :

```bash
    docker exec --interactive --tty sematic-annotation-neo4j cypher-shell -u  neo4j  -p espectateurneo4j "CREATE DATABASE espectateur"
```


## References

    - https://neo4j.com/docs/operations-manual/4.4/backup-restore/restore-dump/
    - https://neo4j.com/docs/cypher-manual/4.4/databases/#administration-databases-stop-database