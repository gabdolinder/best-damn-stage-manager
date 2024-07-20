# Preparing the application
Before building and starting the container, the following needs to be done

### Create environment variables
Environment variables needs to be set in a file called .env
```bash
POSTGRES_USER=
POSTGRES_PW=
POSTGRES_DB=
PGADMIN_MAIL=
PGADMIN_PW=
TR_DOMAIN_NAME=
TR_EMAIL=
TR_AUTH=
```

### Create traefik user password hash
The format per user is ```user:hashed-password```, hashing is preferably done with Bcrypt using the following command in linux ```htpasswd -nbBC 10 USER PASSWORD``` (replace USER and PASSWORD with your own credentials)

# Building and running the application
When you're ready, start the application in daemon mode by running:
`docker compose up --build -d`.