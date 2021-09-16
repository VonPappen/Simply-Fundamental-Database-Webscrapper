FROM python:latest
ENV PYTHONUNBUFFERED=1
RUN pip install psycopg2
COPY . ./code
WORKDIR /code
RUN pip install -r requirements.txt
RUN pip install requests
RUN pip install beautifulsoup4
RUN pip install pandas
RUN pip install openpyxl
RUN pip install lxml
RUN pip install html5lib


# CRON SETUP
# Add crontab file in the cron directory
ADD crontab /etc/cron.d/hello-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/hello-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

#Install Cron
RUN apt-get update
RUN apt-get -y install cron

# RUN chmod -R 777 /code/
# RUN chmod 777 /code/securities_table/initialize_sec_table_v2.py

# RUN /usr/bin/crontab /etc/cron.d/hello-cron
# CMD ["cron", "-f"]


# Run the command on container startup
CMD cron && tail -f /var/log/cron.log