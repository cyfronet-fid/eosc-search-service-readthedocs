# EOSC Search Service

## Running with docker

Run `docker-compose up`.


## Solr

To run a standalone Solr instance run: `docker-compose up -d solr`.
It creates two cores: `ess` and `marketplace`.

To access the web interface go to http://localhost:8983/solr.

Obtain an example data sample using for example selects from
https://docs.cyfronet.pl/display/FID/OpenAire+indexable+data.

Below assumes that Solr instance is available under localhost:8983, i.e. the port 8983
is forwarded to host network.

### mock-dump-1

Then, to load an example dataset, stored in CSV:
```
docker run --rm -v "$PWD/data.csv:/mydata/data.csv" \
           --network=host \
           solr:8.11 \
           post -c ess /mydata/data.csv
```

### mock-dump-2

Either use directly the jsonl file or transform the original using (assuming the file is placed in `tmp/000017_0`):
```
python transform/tsv-to-jsonl-1.py tmp/000017_0 > tmp/000017_0.jsonl
```

Then, load such a sanitized dataset:
```
docker run --rm -v "$PWD/tmp/000017_0.jsonl:/mydata/data.jsonl" \
           --network=host \
           solr:8.11 \
           post -c ess /mydata/data.jsonl
```


## Running RS locally

Check-out the code from
https://git.man.poznan.pl/stash/scm/eosc-rs/online-ml-ai-engine.git
(commit ea3545a6fc3 at the time of writing) to a separate directory, and
build the image:
```shell
docker build -t "omae:0.0.1" .
```

Then, run the image:
```shell
docker run -p 9080:80 omae:0.0.1
```


## Deployment

There are to be two machines, one for db and api, another for solr (see
docker-compose.yml for components).

`api` envs:
- `DATABASE_URI`, in format: `postgresql+psycopg2://<db_user>:<db_password>@db:5432/<db_name>`
- `SOLR_URL`, for example `http://solr.domain:8983/solr/`

`db` envs:
- `DB_POSTGRES_DB`
- `DB_POSTGRES_USER`
- `DB_POSTGRES_PASSWORD`

`solr` doesn't have any envs.

### DB migration

DB has to be migrated after code changes, to do it run alembic in the
`/backend/Dockerfile` image, setting the `DATABASE_URI` env.

```shell
docker run --rm \
           --network "<ess-local_network>" \
           -e "DATABASE_URI=<as_for_api_above>" \
           -it $(docker build -q ./backend) \
           pipenv run alembic upgrade head
```


### DB seed

Add the default dump content by running:
```shell
docker run --rm \
           --network "<ess-local_network>" \
           -e "DATABASE_URI=<as_for_api_above>" \
           -it $(docker build -q ./backend) \
           pipenv run python -m app.manager db seed-oag-1
```


### Solr

It should be placed on another machine. We don't use SolrCloud for now, only
a single-instance installation.

To populate the default core `ess`, follow the guide from the section Solr above.
The link to the sample data is in a comment to
https://docs.cyfronet.pl/display/FID/OpenAire+indexable+data, for now only import
`publications_0.csv` this way.

## Releasing

To create a release commit use the [standard-version](https://github.com/conventional-changelog/standard-version).

To create a release:
```
npx standard-version
```
It will update the changelog and create a tag (according to the Conventional Commits spec).

Then you have to push the tag and the commit to the remote.

On pushing to remote a release with an extended changelog should be created.