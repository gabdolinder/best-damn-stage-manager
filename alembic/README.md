# Alembic 
Is the tool that handles the database migrations

## How to create a migration

The first step is to make the wanted changes in the ``models.py`` file, making the same changes in the ``schemas.py`` file is not strictly necessary but it's good practice since then the tables in the database match the pydantic set up.

Next step is to create the migration, you do this by running the following command
```bash
docker-compose run --rm bdsm-migrate alembic revision --autogenerate -m "Migration description"
```
This will autogenerate a file in the ``alembic/versions`` folder that states the changes that will be made to the database, make sure they are the wanted changes.

### Important!!!
Some changes made will lead to the tables being destroyed and built up again, so if there is important data make sure to save it somewhere so you won't loose it.

To implement your wanted changes run the following command

```bash
docker-compose run --rm bdsm-migrate alembic upgrade head
```

When the migration has been done it's good practice to check in the databse that it went through, log into the database by running the following command

```bash
docker exec -it <postgres-container-name> psql -U <postgres-user>
```
And then check the wanted table. 


## Other good commands
```bash
# Look at the history of changes
docker-compose run --rm bdsm-migrate alembic history
# Rollback the last change
docker-compose run --rm bdsm-migrate alembic downgrade -1
```

## Oh no, I deleted the version files and now I get an error!
It happens to the best of all, what you do is that you log into the database

```bash
docker exec -it <postgres-container-name> psql -U <postgres-user>
# You select the alembic version table
select * from alembic_version ;
# Remove the id from the table
delete from alembic_version where version_num ='<whatever-id>'
```
