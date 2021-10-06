import os

# USE LOCALLY
# USERNAME        = "postgres"
# PASSWORD        = "postgres"
# HOST            = "localhost"
# PORT            = "5432" # os.getenv("POSTGRES_PORT")
# DATABASE_NAME   = "postgres"



# AWS RDS
USERNAME        ='postgres'
PASSWORD        ='postgres5678'
PORT            =5432
DATABASE_NAME   ='webscrapping'
HOST            ='database-webscrap.ccaaerr6cq44.eu-west-3.rds.amazonaws.com'

# USE WITH DOCKER
# Set these values to an environment variable
# USERNAME        = os.getenv("POSTGRES_USER")#"postgres"
# PASSWORD        = os.getenv("POSTGRES_PASSWORD")#"postgres"
# HOST            = os.getenv("POSTGRES_HOST")#"localhost"
# PORT            = os.getenv("POSTGRES_PORT") # os.getenv("POSTGRES_PORT")
# DATABASE_NAME   = os.getenv("POSTGRES_DB")

# Scheme: "postgresql+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
DATABASE_URI = f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"
