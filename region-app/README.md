# Region-app

## Design considerations
- Flask Blueprints are overkill in this case and often cause scaling issues if there is need for common models.
- Using a library like Flask-RESTful will be skipped because it locks you into the framework which causes issues with coupling, handling super-resources, and really works best only with simple CRUD apps, which most applications evolve not to be.
- Due to the external API being consumed, FastApi could be used (which is asynchronous) with very few modifications to this codebase, FastApi also has the advantage of being self documenting with the ability to create its own openApi specification.
- Tests are created and run using `unittest` as opposed to `pytest`. `unittest` is powerful and robust, and this current case, the useful parts of `pytest` aren't required.
- The CSV will be used to populate database, this can be done at any point.

### Architecture
The application is split into `controllers`, `models`, and `serialisers`. Typically, one would also add a `service` and `dao` layer, but in this example, the benefits of these extra layers wouldn't be clear and instead would appear to just add extra boiler-plate code.

#### Design notes:
- Models will be Flask-SQLAlchemy based, its a well document library
- Controllers take the request and perform the business logic. The service would usually perform the business logic, while the controller would just consume the service, allowing a decoupling of the flask request interface with our business code. Having a service layer is useful when you have super-resources that encapsulate sub resources. Fortunately, it's not costly to refactor a service layer when it is required.
- Serialisers are part of the presentation layer. A serialiser takes an instance of a model and converts it into a dictionary that is able to serialised by the `flask.jsonify` function. The name itself is a misnomer, because it doesn't actually serialise.
- The model tables are created in the database at run-time if they aren't already present. This is not how I would handle this in production. One could use something like `Flask-Migrate` to handle the database migrations, however I consider this as step in the wrong direction as it overly couples your DBA setup with the ORM you are using. A better approach from my perspective would be to have an external DBA repo with its own tooling for handling migrations. The database should be versioned and considered like any other component.

## Installation
```
# Create and activate your given env (conda, venv, etc)
...

# Install the dependencies
pip install -r requirements.txt
```

## Testing
This goes through how to run the unittests.
```
python -m unittest discover -p "*_test.py"
```

## Deployment
This shows how to deploy this specific application on local without using Docker. In this case, we will deploy using an sqlite3 database. For simplicity, and the ability to use Flask hot reload tool, we will deploy simply using the Flask builtin server (though this shouldn't be done in a production environment).
```
# This command will deploy the application on localhost:8080
export db_uri="sqlite:///app.sqlite3"
python main.py
```

## Seeding the database
To seed the database with data from a CSV file, run the following command with the `<` and `>`.
```
flask seed <path_to_csv>
```
Once seeded, the database can't be re-seeded from the same dataset currently as the seeding script doesn't handle repopulation and updating.

# Things to improve
- The seeding script could be updated to allow for re-seeding with the same dataset, allowing existing rows to be updated with new values, and allowing new rows to be added.
- ...
