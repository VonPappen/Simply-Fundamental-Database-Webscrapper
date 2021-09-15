import os

# USE LOCALLY
USERNAME        = "postgres"
PASSWORD        = "postgres"
IP_ADRESS       = "localhost"
PORT            = "5432" # os.getenv("POSTGRES_PORT")
DATABASE_NAME   = "postgres"


# USE WITH DOCKER
# Set these values to an environment variable
# USERNAME        = os.getenv("POSTGRES_USER")#"postgres"
# PASSWORD        = os.getenv("POSTGRES_PASSWORD")#"postgres"
# IP_ADRESS       = os.getenv("POSTGRES_USER")#"localhost"
# PORT            = "5432" # os.getenv("POSTGRES_PORT")
# DATABASE_NAME   = "postgres"

# Scheme: "postgresql+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
DATABASE_URI = f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{IP_ADRESS}:{PORT}/{DATABASE_NAME}"
