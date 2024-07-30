# Preparing the application
Before building and starting the container, the following needs to be done

### Create environment variables
Environment variables needs to be set in a file called .env
```bash
POSTGRES_USER=
POSTGRES_PW=
POSTGRES_DB=
POSTGRES_PORT=
POSTGRES_CONTAINER_NAME=
PGADMIN_MAIL=
PGADMIN_PW=
TR_DOMAIN_NAME=
TR_EMAIL=
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PW}@db/${POSTGRES_DB}
ALEMBIC_DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PW}@${POSTGRES_CONTAINER_NAME}:${POSTGRES_PORT}/${POSTGRES_DB}
```

### Add users and passwords for the digestauth
For now the auth system is very crude and quite horrible, but it works.
Simply run the following command (with -c if no file exists, without -c to add another user to an existing file)
`htdigest -c <name of file> traefik <username>`


# Building and running the application
When you're ready, start the application in daemon mode by running:
`docker compose up --build -d`.