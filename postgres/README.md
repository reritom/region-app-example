# Postgres service
The purpose of this service is to be used as the database server for our region-app service.
In a production environment, we are unlikely to use Sqlite3, and more like to use something similar to Postgres.

This directory is for creating Postgres image with a dedicated database for our region app. Note the username and password in the init.sql are insecure, as handling of that area is out of the scope of this example.
