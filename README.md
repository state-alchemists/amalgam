# Amalgam

In this demo, you will see how you can use [Zrb](https://pypi.org/project/zrb) to:

- Create a modular-monolith CRUD application.
- Add some entities/fields.
- Run the application as monolith/microservices.

No coding skill is required.

# Start the demo

Before starting the demo, you need to make sure you have the following software installed:

- Python (3.10 or higher)
- Pip
- Venv
- Zrb

Once everything is set, you can run the following script on your terminal:

```bash
./init.sh
```

The commands will give you:

- A folder named `my-project`.
- A Python application under the project (`my-project/src/myapp`).
- A `library` module under the application (`myproject/src/myapp/src/module/library`)
- A `book` entity under the `library` module.
- A field named `title` under the `book` entity.

It will also run the application on your local computer.

# Open myapp from the browser

You can visit [http://localhost:3000](http://localhost:3000) to see how the application works.

The default username and password will be `root` and `toor`.

Try to add some books.

![](images/my-app-list-of-book.png)

# Override default username and password

You can override the system username and password by setting some environment variables:

```bash
# press ctrl + c to stop the application
export MYAPP_APP_AUTH_ADMIN_USERNAME=gofrendi
export MYAPP_APP_AUTH_ADMIN_PASSWORD=aVeryStrongPassword73
zrb project myapp monolith start 
```

# Checking the process

Currently, `myapp` is running as a single process on your local computer.

Let's confirm this by opening a new terminal and invoking the following command:

```bash
pgrep fastapi -a
```

You should see a single process like this:

```
46252 ... fastapi dev main.py --port 3000
```

# Run Myapp as Microservices

Now let's go back to your first terminal; so that you can kill `my-app` process by pressing `ctrl + c`.

Stay in your first terminal, and try to invoke the following command:

```bash
zrb project myapp microservices start
```

Once started, you will be able to access [http://localhost:3000](http://localhost:3000) as you have done previously.

Now let's invoke the following command on your second terminal:

```bash
pgrep fastapi -a
```

```
46252 ... fastapi dev main.py --port 3001
46254 ... fastapi dev main.py --port 3002
46256 ... fastapi dev main.py --port 3003
```

You can see that now you have multiple processes.

Each process handles different aspect of the application:

- `myapp-gateway` (port: 3001)
    - Handle HTTP requests from user
    - Send HTTP requests to other services
- `myapp-auth-service` (port: 3002)
    - Handle and reply HTTP requests from gateway
- `myapp-library-service` (port: 3003)
    - Handle and reply HTTP requests from gateway

You can see that you can run `myapp` as either microservices or as a Monolith.
