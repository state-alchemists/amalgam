# Myapp

Myapp is a modular monolith application built on top of [FastApi](https://fastapi.tiangolo.com/) and [Svelte Kit](https://kit.svelte.dev/).

You can run Myapp as a monolith or microservices.

Running your application as a monolith is preferable during local development. Furthermore, monolith application is more maintainable than microservices.

The purpose of Myapp is to:

- Give you a sensible default.
- Give you a good experience while developing/testing things locally.
- Assure you that your application is always ready to be deployed as microservices.

You can learn more about Myapp's modular monolith concept in our [documentation](docs/modular-monolith/README.md).

# Run Myapp as a monolith

To run Myapp as a monolith, you can invoke the following command:

```bash
zrb project myapp monolith start
```

You can also run Myapp as a docker container by invoking the following command:

```bash
zrb project myapp-container container monolith start
```

# Run Myapp as a microservices

To run Myapp as a microservices, you can invoke the following command:

```bash
zrb project myapp microservices start
```

You can also run Myapp as a docker container by invoking the following command:

```bash
zrb project myapp-container microservices start
```

# Accessing the web interface

Once you start the application, you can visit [`http://localhost:3000`](http://localhost:3000) in your browser. By default, the application will run on port 3000, but you can change the port by providing `MYAPP_APP_PORT`.

To log in as admin, you can use the following credential:

- User: `root`
- Password: `toor`

You can change the default username and password by providing `MYAPP_APP_AUTH_ADMIN_USERNAME` and `MYAPP_APP_AUTH_ADMIN_PASSWORD`.

Furthermore, you can also visit `http://localhost:3000/docs` to access the API specification.

# Deploying to Kubernetes

To deploy Myapp to Kubernetes, you need to have [Pulumi](https://www.pulumi.com/) installed. You also need access to a container registry like [Docker Hub](https://hub.docker.com/) and to the Kubernetes cluster itself.

The easiest way to set up Kubernetes on your local computer is by installing [Docker Desktop](https://www.docker.com/products/docker-desktop/). Once you installed Docker Desktop, you can go to `setting | Kubernetes` to enable your local Kubernetes cluster.

Finally, you can invoke the following command:

```bash
# Deploy Myapp to Kubernetes as a monolith
zrb project myapp monolith deploy

# Deploy Myapp to Kubernetes as a microservices
zrb project myapp microservices deploy
```

# Configuration

You can see all available configurations on [`template.env`](src/template.env). If you need to override the configuration, you can provide environment variables with `MYAPP_` prefix to the ones specified in the `template.env`.

There are several configurations you need to know.

Auth related config

- `MYAPP_APP_AUTH_ADMIN_ACTIVE`: determine whether there is an admin user or not
    - default value: `true`
- `MYAPP_ADMIN_USERNAME`: Admin username
    - default value: `root`
- `MYAPP_ADMIN_PASSWORD`: Admin password
    - default value: `toor`
- `MYAPP_APP_PORT`: Application port
    - default value: `3000`

Messaging config:

- `MYAPP_APP_BROKER_TYPE`: Messaging platform to be used (i.e., `rabbitmq`, `kafka`, or `mock`)
    - default value: `rabbitmq`

Feature flags:

- `MYAPP_APP_ENABLE_EVENT_HANDLER`: Whether enable event handler or not
    - default value: `true`
- `MYAPP_APP_ENABLE_RPC_SERVER`: Whether enable RPC server or not
    - default value: `true`
- `MYAPP_APP_ENABLE_FRONTEND`: Whether enable Frontend or not
    - default value: `true`
- `MYAPP_APP_ENABLE_API`: Whether enable API or not
    - default value: `true`
- `MYAPP_APP_ENABLE_AUTH_MODULE`: Whether enable Auth module or not
    - default value: `true`
- `MYAPP_APP_ENABLE_LOG_MODULE`: Whether enable Log module or not
    - default value: `true`
- `MYAPP_APP_ENABLE_<MODULE_NAME>_MODULE`: Whether enable `<MODULE_NAME>` module or not
    - default value: `true`


# Adding modules, entities, or fields

There are CLI commands to help you add modules, entities, and fields into Myapp.

For simple CRUD, you won't need to code at all. Please see [Zrb tutorial](https://github.com/state-alchemists/zrb/blob/main/docs/tutorials/development-to-deployment-low-code.md) for more details.


# Prerequisites

Main prerequisites

- Python 3.10 or higher
- Pip
- Venv
- Node version 18 or higher
- Npm

If you want to run Myapp on containers, you will also need `Docker` with the `Docker-compose` plugin.

You will also need `Pulumi` if you want to deploy Myapp into your Kubernetes cluster.

# Directory Structure

- `docker-compose.yml`: A multi-profile docker-compose file. This helps you to run your application as a monolith/microservices.
- `all-module-disabled.env`: Feature flags to be used when you deactivate all modules.
- `all-module-enabled.env`: Feature flags to be used when you activate all modules.
- `deployment/`: Deployment directory. By default, we put deployment along with the source code to make it easier to maintain/manage. You can later move your deployments to another repository if you think you need to.
    - `/helm-charts`: Helm charts for Rabbitmq, Redpanda, and Postgre.
    - `__main__.py`: Main Pulumi script.
    - `template.env`: Default configuration for deployment
- `src/`: Myapp source code, including backend and frontend.
    - `Dockerfile`: Dockerfile to build Myapp
    - `template.env`: Default configuration to run Myapp
    - `requirements.txt`: Pip packages, list of Myapp dependencies. If you need to use external libraries in Myapp, make sure to list them here.
    - `main.py`: Myapp's application entry point. This module exposes an `app` object that will be picked up by Uvicorn.
    - `config.py`: Myapp's configuration loader.
    - `migrate.py`: A script to perform database migration.
    - `integration/`: Initialization of components you want to use in your application. Typically containing scripts to instantiate `app` objects, DB connections, Message bus connections, etc. This is where you create and connect components.
    - `component/`: Interface and component class definitions.
    - `frontend/`: Frontend source code
        - `package.json`: NPM configuration for Myapp frontend.
        - `svelte.config.json`: Svelte configuration.
        - `tailwind.config.json`: Tailwind configuration.
        - `vite.config.ts`: Vite configuration.
        - `src/`: Myapp frontend source code.
            - `lib/`: Frontend components and helpers.
            - `routes/`: Frontend page definitions.
        - `build/`: Frontend build result.
        - `static/`: Static files like images, favicon, etc.
    - `helper/`: Common helper scripts. Typically stateless.
    - `schema/`: Common Pydantic schemas.
    - `module/`: Module definition. Each module can be deployed as a microservice. Thus, modules should be isolated from each other.
        - `<module_name>/`: Module resources.
            - `api.py`: HTTP request handler for the current module.
            - `event.py`: Event handler for the current module.
            - `rpc.py`: RPC handler for the current module.
            - `register_module.py`: A script to register the module to the main application.
            - `migrate.py`: A script to perform migration for the current module.
            - `integration/`: Initialization of components for the current module.
                - `model/`
                - `repo/`
            - `component/`: Interface and component class definition for the current module.
            - `entity/`: Entity related resources.
                - `<entity_name>/`: Resources for current entity.
                    - `api.py`
                    - `rpc.py`
                    - `model.py`
                    - `repo.py`
            - `schema/`: Pydantic schemas for the current module.
- `test/`: Test scripts.
    - `<modules-name>/`: Test scripts for modules.
    - `test_*.py`: Core test scripts.


# Decisions and Constraints

## Frontend
- Myapp's Frontend is served as static files and is built before runtime (not SSR/Server Side Rendering). That's mean.
    - The SEO is probably not good.
    - The page load is sensibly good.
- We use Svelte for Frontend because it is easier to read/learn compared to React, Vue, or Angular.
- At the moment, the frontend use:
    - Sveltekit
    - TailwindCSS
    - DaisyUI

## Database

- Myapp uses SQLAlchemy to handle
    - Database connection
    - Database migration
    - Data manipulation
- To create a custom database implementation, you need to create an implementation that complies with `core.repo.Repo`.

## Messaging

- Currently, Myapp supports some messaging platforms:
    - Rabbitmq (default):
        - `APP_BROKER_TYPE=rabbitmq`
    - Kafka/Redpanda
        - `APP_BROKER_TYPE=kafka`
    - No messaging platform, a.k.a: in memory. This will only work properly if you run Myapp as a monolith.
        - `APP_BROKER_TYPE=mock`
- To create custom event handlers, you need to implement two interfaces:
    - `core.messagebus.Publisher`
    - `core.messagebus.Server`

## RPC

- Currently, RPC implementation depends on the messaging platforms. It is possible to override this behavior by creating you custom implementation. There are two interfaces you need to override:
    - `core.rpc.Caller`
    - `core.rpc.Server`
