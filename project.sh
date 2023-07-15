if [ ! -d ".venv" ]
then
    echo "👷 Create .venv"
    python -m venv .venv
fi

echo "👷 Activate .venv"
source .venv/bin/activate

echo "👷 Install requirements"
pip install -r requirements.txt
