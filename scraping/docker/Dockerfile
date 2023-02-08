# --- Get Python 3 Base Image
FROM python:3

# --- Update Container
RUN apt-get update && apt-get -y install cron vim busybox locales dos2unix

# --- Set Working Directory
WORKDIR /scraping

# --- Copy the crontab to the container
COPY crontab /etc/cron.d/crontab

# --- Remove the DOS Endline Character from the crontab script
RUN dos2unix /etc/cron.d/crontab && apt-get --purge remove -y dos2unix && rm -rf /var/lib/apt/lists/*

# --- Change Execution settings of crontab
RUN chmod 0644 /etc/cron.d/crontab

# --- Copy the Python Files to the container
COPY data_cleaning.py /scraping/data_cleaning.py
COPY scrape_data.py /scraping/scrape_data.py

# --- Copy requirements.txt file to container
COPY requirements.txt ./requirements.txt

# --- Run command line instructions
RUN pip install -r requirements.txt

# --- Make Python file executable
RUN chmod 0744 /scraping/data_cleaning.py

# --- Runs the Cron Service
RUN /usr/bin/crontab /etc/cron.d/crontab

CMD  busybox syslogd -C; cron -L 2 -f