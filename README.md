# GenderGP Take Home Assessment

## Setup

### 1. Update .env

Run these commands from project root

```sh
$ cp .env.sample .env

# Generate your secret key
$ openssl rand -hex 32
```

### 2. Seeding

Seed some scripts for data generation

`$ python  seed.py`

`$ scripts/seed_patients.py`

`$ scripts/seed_users.py`

`$ scripts/seed_prescriptions.py`

### 3. Running

```sh

docker compose up -d
fastapi dev
```

API will be running on localhost:8000

### Docs

FastAPI has docs built-in, you can view them at `localhost:8000/docs`

### Auth

As this is just a demo, [FastAPI Users](https://fastapi-users.github.io/fastapi-users/latest/) has been used for quick jwt to protect routes.
In the real world, the jwt would have already flown through the request and then validated in the jwt middleware in the api layer.
Permissions wise, these would be embedded into the JWT as the users role & permissions would ideally come from cognito user pool attribs.
