FROM python:3

WORKDIR /api

COPY requirements.txt ./requirements.txt

# --- Run command line instructions
RUN pip3 install -r requirements.txt

# --- Copy all files from local project to Docker Image
COPY . .

EXPOSE 8000
