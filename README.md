# Example application
## Purpose
The purpose of this application is to store and display data related to Frencnh cities, counties, and regions.
The region-app Flask app can be run locally (without docker) using Sqlite3 as a database, to do so, navigate to its readme, listed below. The application can also be deployed using Docker, backed by a PostGres instance, to do that, follow this readme.

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
If you get the following error in your docker-compose logs, run `chmod +x region-app/await_postgres.sh`.
```
region-app_1  | sh: ./await_postgres.sh: Permission denied
```

### Local testing (perhaps for looking into production bugs)
In this case, we want to use the absolute version of our application (whichever version is in prod), so we will take the correct version from github (in this example we haven't handled versioning, so we will just take the most recent commit from the repo). The aforementioned logic is handled by the docker-compose file.
```
docker-compose -f docker-compose.yaml up -V --build --force-recreate
```

### Seeding
To seed the docker deployed instance of the application, get the region-app container id by using `docker ps`
```
docker exec <container_id> flask seed static/correspondance-code-insee-code-postal.csv
```
Note: I haven't explicitly added any persistent volumes for the database in this example, so when you redeploy, you will need to re-seed.

## Notes
### Things that slowed me down
- Parsing the CSV was a bit slow when creating the models due to the nature checking which field in which model should be represented by which column from the CSV dataset
- I haven't made a feeding script with Flask before, and in doing so, it prevented the design pattern that I usually use when handling creating application instances with different database uris, which meant I had to access the db_uri from the os.environ, instead of passing it as an argument to the create_app factory. This has further consequences related to how I handle db_uris with the Dockerfile and the docker-compose files.

### Things to improve on the deployment level
- Due to the changes I had to make to handle the seeding cli, which meant using db_uri in the environment, my docker-compose files pass the db_uri to the Dockerfile as an arg. This means the PostGres db_uri, including the username and password, are visible in the docker-compose.yaml. Really these should use `secrets` if this were to be improved.
