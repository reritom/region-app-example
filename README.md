# Example application
## Purpose
...

## Services
Note: Each service has a nested README which contains more details and can be found by clicking the links below.
- ![Region-App](region-app/README.md)
- ![PostGres](postgres/README.md)

## Deployment
### Local development with Docker
In local development, using sqlite3 practically makes little difference. But sometimes we want our environment to reflect the production environment as much as possible, so we need to run a PostGres server on local, and in that case we might as well deploy the complete application in local with Docker.

Obviously you'll need Docker installed for this for work.

This command will mount your local source code as volumes, so you can develop on the application in real time.
```
docker-compose -f docker-compose.dev.yaml up -V --build --force-recreate
```

### Local testing (perhaps for looking into production bugs)
In this case, we want to use the absolute version of our application (whichever version is in prod), so we will take the correct version from github (in this example we haven't handled versioning, so we will just take the most recent commit from the repo). The aforementioned logic is handled by the docker-compose file.
```
docker-compose -f docker-compose.yaml up -V --build --force-recreate
```
