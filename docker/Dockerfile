# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /kekbosrv

# Copy the current directory contents into the container at /app
COPY kekbosrv.py /kekbosrv
COPY requirements.txt /kekbosrv
COPY MqttConnector.py /kekbosrv
COPY Authenticator.py /kekbosrv

COPY ./sql/init.sql /docker-entrypoint-initdb.d/

# Install the required packages
RUN pip install -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable to make FastAPI run on host 0.0.0.0
ENV HOST=0.0.0.0

# Run FastAPI when the container launches
CMD ["uvicorn", "kekbosrv:app", "--host", "0.0.0.0", "--port", "8000"]
