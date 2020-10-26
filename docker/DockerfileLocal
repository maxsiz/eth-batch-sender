# Use an official Python runtime as a parent image
FROM python:3.7-stretch

# Set the working directory to /app
WORKDIR /app

ADD ./docker/requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the current directory contents into the container at /app

# Run app.py when the container launches
ENTRYPOINT ["python3.7"]