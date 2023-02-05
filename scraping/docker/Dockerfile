# --- Get Python 3 Base Image
FROM python:3

# --- Update Container
RUN apt-get update && apt-get -y install cron vim

# --- Set Working Directory
WORKDIR /scraping

# --- Copy the crontab to the container
COPY crontab /etc/cron.d/crontab

# --- Change Execution settings of crontab
RUN chmod 0644 /etc/cron.d/crontab

# Not sure what this does yet honestly...
RUN /usr/bin/crontab /etc/cron.d/crontab

# --- Copy the Python Files to the container
COPY data_cleaning.py /scraping/data_cleaning.py
COPY scrape_data.py /scraping/scrape_data.py

# --- Copy requirements.txt file to container
COPY requirements.txt ./requirements.txt

# --- Run command line instructions
RUN pip3 install -r requirements.txt

# --- Prints the Python Path
RUN echo $PYTHONPATH
