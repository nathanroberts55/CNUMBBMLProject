# --- Get Python 3 Base Image
FROM python:3

# --- Set Working Directory
WORKDIR /api

# --- Copy requirements.txt file to container
COPY requirements.txt ./requirements.txt

# --- Run command line instructions
RUN pip3 install -r requirements.txt

# --- Copy all files from local project to Docker Image
COPY . .

EXPOSE 8000
