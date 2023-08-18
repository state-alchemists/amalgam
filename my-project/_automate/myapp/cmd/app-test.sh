PYTHONUNBUFFERED=1
PYTHONPATH=$PYTHONPATH:$(pwd)/src
cd src
echo "Activate virtual environment"
source .venv/bin/activate

cd ..
pytest --cov=src --cov-report html --cov-report term --cov-report term-missing {{input.myapp_test}}