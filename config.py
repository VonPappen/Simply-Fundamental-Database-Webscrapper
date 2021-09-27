import os

# USE LOCALLY
# USERNAME        = "postgres"
# PASSWORD        = "postgres"
# HOST            = "localhost"
# PORT            = "5432" # os.getenv("POSTGRES_PORT")
# DATABASE_NAME   = "postgres"


# USE WITH DOCKER
# Set these values to an environment variable
USERNAME        = os.getenv("POSTGRES_USER")#"postgres"
PASSWORD        = os.getenv("POSTGRES_PASSWORD")#"postgres"
HOST            = os.getenv("POSTGRES_HOST")#"localhost"
PORT            = os.getenv("POSTGRES_PORT") # os.getenv("POSTGRES_PORT")
DATABASE_NAME   = os.getenv("PASTGRES_DB")

# Scheme: "postgresql+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
DATABASE_URI = f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"
