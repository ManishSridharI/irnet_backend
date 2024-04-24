# # Use the official lightweight Python image.
# # https://hub.docker.com/_/python
# FROM python:3.7-slim

# # Allow statements and log messages to immediately appear in the Knative logs
# ENV PYTHONUNBUFFERED True

# # Copy local code to the container image.
# ENV APP_HOME /app
# WORKDIR $APP_HOME
# COPY . ./

# # Install production dependencies.
# RUN pip install --no-cache-dir -r requirements.txt

# # Run the web service on container startup. Here we use the gunicorn
# # webserver, with one worker process and 8 threads.
# # For environments with multiple CPU cores, increase the number of workers
# # to be equal to the cores available.
# # Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
# #CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
# CMD ["gunicorn", "--bind", ":9900", "--workers", "1", "--threads", "8", "--timeout", "0", "main:app"]

# Use the official lightweight Python image.
FROM python:3.7-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Set the Flask environment to development to enable auto-reload
ENV FLASK_ENV=development

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
# RUN pip install --no-cache-dir -r requirements.txt

# Install system dependencies required for Anaconda
RUN apt-get update && apt-get install -y wget && apt-get clean

# Download and install Anaconda
RUN wget https://repo.anaconda.com/archive/Anaconda3-2024.02-1-Linux-x86_64.sh -O /anaconda.sh && \
    /bin/bash /anaconda.sh -b -p /opt/conda && \
    rm /anaconda.sh

# Add Anaconda to PATH
ENV PATH /opt/conda/bin:$PATH

# Create the conda environment for IRnet
COPY app/IRnet-main/IRnet_env.yaml /IRnet_env.yaml
RUN conda env create -f /IRnet_env.yaml

# Initialize conda in bash shell
#RUN conda init && . ~/.bashrc && conda activate IRnet_env
#RUN conda activate IRnet_env

# Use the flask command to run the app to take advantage of the reload mechanism
#CMD ["flask", "run", "--host=0.0.0.0", "--port=9900"]

# # Activate the conda environment when running the container
SHELL ["conda", "run", "-n", "IRnet_env", "/bin/bash", "-c"]

# # Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# # Use the flask command to run the app to take advantage of the reload mechanism
CMD ["conda", "run", "-n", "IRnet_env", "flask", "run", "--host=0.0.0.0", "--port=9900"]
RUN conda init && . ~/.bashrc && conda activate IRnet_env
