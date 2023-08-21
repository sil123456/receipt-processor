#Deriving the python 3 base image
FROM python:3

#COPY the remote file at working directory in container
COPY . /app

# Set working directory
WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose a port (if needed)
EXPOSE 8000

# Define the command to run the application
CMD ["python", "app.py"]