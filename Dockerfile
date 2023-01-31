# --- Set base image in python 3.10
FROM python:3

# --- Expose Port 8501 that Streamlit runs on
EXPOSE 8501

# --- Set Working Directory
WORKDIR /app

# --- Copy packages required from Requirements file to Docker Image Requirements file
COPY requirements.txt ./requirements.txt

# --- Run command line instructions
RUN pip3 install -r requirements.txt

# --- Copy all files from local project to Docker Image
COPY . .

# --- Command to run streamlit application
CMD streamlit run app/app.py
