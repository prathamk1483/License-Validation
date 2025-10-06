echo "Deployment started"

python3.13 -m venv env

source env/bin/activate

echo "Environment created"

pip install --upgrade pip
pip install Django==5.2.7 sqlparse==0.5.3 tzdata==2025.2 djangorestframework==3.16.1

echo "Installing PsycoPG"
pip install psycopg2-binary


python manage.py collectstatic --noinput

echo "Deployment completed"