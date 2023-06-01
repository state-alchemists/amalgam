# Fastapp

A FastAPI application created by using `zrb`.

# Prerequisites

Main prerequisites

- Internet connection (to download pip/npm packages)
- Python 3.9
- Pip
- Venv
- Node version 18
- Npm

Optional prerequisites

- Docker
- Docker-compose
- Zrb
- Pulumi

# How to run Fastapp


## Manually

Before running the server, you need to build the front end:

```bash
# If you are currently in `src/fastapp/src` directory,
# you need to move to frontend
cd frontend

# Install node modules
npm install --save-dev

# Build frontend (the build artefact will be available at `frontend/build`)
npm run build:watch
```

Once you build the front end, you should open a new terminal/TMUX panel to run the server.

To run the server you can do the following:

```bash
# Make sure you are in src/fastapp/src` directory

# Create virtual environment if not exists
if [ ! -d "venv" ]
then
    python -m venv venv
fi

# Install pip packages
pip install -r requirements.txt

# By default zrb expect you have rabbitmq at localhost:5672
# If you don't have rabbitmq, you can use `mock` broker
export FASTAPP_APP_BROKER_TYPE=mock

# Run Fastapp using uvicorn and auto-reload
uvicon main:app --host 0.0.0.0 --port 8080 --reload
```

You will be able to access Fastapp by accessing `http://localhost:8080` from your browser.

### Note about Frontend

We use sveltekit + tailwind. W follow these guides to set up the Frontend:

- [Install Tailwind CSS with Sveltekit](https://tailwindcss.com/docs/guides/sveltekit)
- [Sveltekit static site generation](https://kit.svelte.dev/docs/adapter-static)

## Using Zrb

To run Fastapp using `zrb`, you need to activate `zrb` project environment.

First, make sure you are currently in the project directory, then load `project.sh`

```bash
# If you are currently in `src/fastapp/src` directory,
# you need to move to project directory

cd ../../..
source project.sh
```

Once you activate `zrb` project environment, you can run Fastapp by invoking the following:

```bash
zrb project start fastapp
```

This will run a docker container as well as build the front end and run the server.

You can also run Fastapp as a container:

```bash
zrb project start fastapp-container
```
