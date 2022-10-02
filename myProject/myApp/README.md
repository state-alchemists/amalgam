# MyApp

`MyApp` is a microservice-ready monolith application.

This application is created using [Zaruba](https://github.com/state-alchemists/zaruba). To create the application, you can invoke:

```bash
zaruba please initProject # or cd to your zaruba project
zaruba please addFastApp appDirectory=myApp

# zaruba please start
```

# 🏁 How to start

You can run `myApp` by invoking:

```bash
zaruba please startMyApp
```

Alternatively, you can also invoke the following script:

```bash
cd myApp

# create virtual environment if not exist
if [ ! -d ./venv ]; then python -m venv ./venv; fi

# activate virtual environment
source venv/bin/activate

# install pip packages
pip install -r requirements.txt

# load environments
source template.env

# run the application
./start.sh
```

# 🧪 How to test

You can run `myApp` unit-test by invoking:

```bash
zaruba please testMyApp
```

Alternatively, you can also invoke the following script:

```bash
cd myApp

# create virtual environment if not exist
if [ ! -d ./venv ]; then python -m venv ./venv; fi

# activate virtual environment
source venv/bin/activate

# install pip packages
pip install -r requirements.txt

# load environments
source template.env

# run pytest
pytest -rP -v --cov="$(pwd)" --cov-report html
```

# ☑️ Prerequisites

- Python 3.9
- Pip
- Virtual env

# 📖 Documentation

Please visit MyApp documentation [here](_docs/README.md).