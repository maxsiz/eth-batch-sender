# Use an official Python runtime as a parent image
FROM python:3.7-stretch

# Set the working directory to /app
WORKDIR /app

ADD ./docker/requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the current directory contents into the container at /app
ADD ./web3/web3worker.py /app
ADD ./web3/config.py /app
ADD ./web3/exotoken.abi /app

# Run app.py when the container launches
CMD ["python3", "web3worker.py"]