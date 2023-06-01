# MyProject

This is a Zrb project.

To learn more about Zrb, please visit the [Zrb homepage](https://pypi.org/project/zrb/).

# MyProject Directory Structure

```
.
    _automate/
        <your-automation-script>.py
    src/
        <your-source-code>
    .gitignore
    project.sh
    README.md
    requirements.txt
    template.env
    venv
    zrb_init.py
```

All automation scripts should be put in `_automate` directory and should be imported at `zrb_init.py`.

All other resources like application source code, Dockerfile, Helm charts, etc should be located under `src`.

If your automation script depends on third-party pip packages, add them to `requirements.txt`. To get more information about your existing pip package, you can do:

```bash
pip freeze
# or to get specified package information (e.g., dbt):
pip freeze | grep dbt
```

# Activating MyProject

```bash
source ./project.sh
zrb
```

Once you invoke the command, MyProject virtual environment will be created.

# MyProject Configurations

See [template.env](template.env)

To make your configuration, please copy `template.env` to `.env`


# Reloading MyProject Configurations

To reload your configurations, you can invoke the following command:

```bash
reload
```

Please note that MyProject's virtual environment has to be activated first.

# Getting task environments

To get task environments, you can invoke the following command:

```bash
zrb project get-default-env
```

It is expected to use the command for informational purposes only.
You should only override necessary environment variables to keep track of what you need to change.

Being said so, you can also add the default task environments to `.env` by invoking the following command:

```bash
zrb project get-default-env >> .env
```
