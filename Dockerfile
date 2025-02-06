# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies
RUN pip install -r requirements.txt

# Expose a port (e.g., for Flask)
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
