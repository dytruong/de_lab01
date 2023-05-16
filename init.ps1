#/bin/bash

# Download the docker-compose.yaml file
# For linux
#curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'

# For Windows
Invoke-WebRequest -Uri 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml' -OutFile docker-compose.yml

# Make expected directories and set an expected environment variable
#mkdir -p ./dags ./logs ./plugins
New-Item -ItemType Directory -Path "dags", "logs", "plugins"

#echo -e "AIRFLOW_UID=$(id -u)" > .env
Set-Content -NoNewline -Path ".env" -Value "AIRFLOW_UID=50000"

# Initialize the database
docker-compose up airflow-init

# Start up all services
docker-compose up -d