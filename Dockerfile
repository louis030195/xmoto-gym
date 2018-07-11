# Use an official Python runtime as a parent image
FROM python:2.7-slim

COPY requirements.txt ~/desktop/app/

# Set the working directory to /app
WORKDIR ~/desktop/app/

# Copy the current directory contents into the container at /app
ADD . ~/desktop/app/

# Because of pyautogui error
# RUN pip install python3_xlib

# Install any needed packages specified in requirements.txt
# RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Install xmoto
RUN apt-get update
# Need to set -y in dockerfile and -qq is used to delete output
RUN apt-get -qq -y install xmoto

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME Xmoto-v0

# Run app.py when the container launches
CMD ["xmoto"]
# CMD ["python", "dqn2.py"]
