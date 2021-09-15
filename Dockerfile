FROM python:latest
RUN pip install psycopg2
COPY . .
WORKDIR .
RUN pip install -r requirements.txt
RUN python crud.py
# ENV =value