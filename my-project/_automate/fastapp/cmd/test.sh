PYTHONUNBUFFERED=1
PYTHONPATH=$PYTHONPATH:$(pwd)/src
cd src
echo "Activate venv"
source venv/bin/activate

cd ..
pytest --cov=src --cov-report html --cov-report term --cov-report term-missing {{input.fastapp_test}}