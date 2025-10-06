echo "Deployment started"

python3.13 -m venv env

source env/bin/activate

echo "Environment created"

pip install --upgrade pip
pip install -r requirements.txt

echo "Installing PsycoPG"
pip install psycopg2-binary==2.9.10


python manage.py collectstatic --noinput

echo "Deployment completed"