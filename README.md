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
Once deployed, if you make any changes in `region-app/app`, it will trigger `gunicorn` to reload the application, allowing your changes to be present immediately. This is useful for rapid development and bug fixing.

### Local stable deployment
In this case, we want to use an absolute version of our application. Ideally, if this application had its own repo, the docker-compose would build directly from their based on whichever version we want to deploy, but for now it uses the local directory too.
```
docker-compose -f docker-compose.yaml up -V --build --force-recreate
```

### Seeding
To seed the docker deployed instance of the application, get the region-app container id by using `docker ps`
```
docker exec <container_id> flask seed static/correspondance-code-insee-code-postal.csv
```
Note: I haven't explicitly added any persistent volumes for the database in this example, so when you redeploy, you will need to re-seed (if you used the command I provided above, because this explicitly cleans volumes, which is again for easing development).

### Targeting
Once the application is deployed and seeded, you should be able to target it on `127.0.0.1:8080/api/regions`. Additionally, one can use pagination as such `127.0.0.1:8080/api/regions?limit=5&page=1`, where `limit` is the number of items to show per page, and `page` is the page number. The first request will be slower as it will handle caching the external API calls. The subsequent calls will be immediate.

## Notes
### Things that slowed me down
- Parsing the CSV was a bit slow when creating the models due to the nature checking which field in which model should be represented by which column from the CSV dataset
- I haven't made a feeding script with Flask before, and in doing so, it prevented the design pattern that I usually use when handling creating application instances with different database uris, which meant I had to access the db_uri from the os.environ, instead of passing it as an argument to the create_app factory. This has further consequences related to how I handle db_uris with the Dockerfile and the docker-compose files.

### Things to improve on the deployment level
- Due to the changes I had to make to handle the seeding cli, which meant using db_uri in the environment, my docker-compose files pass the db_uri to the Dockerfile as an arg. This means the PostGres db_uri, including the username and password, are visible in the docker-compose.yaml. Really these should use `secrets` if this were to be improved.
