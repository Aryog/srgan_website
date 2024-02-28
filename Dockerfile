# Use a base Python image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the Flask application code into the container
COPY . /app

# Install required dependencies
RUN pip install -r requirements.txt

# Expose the Flask application port
EXPOSE 3000

# Specify the command to run the Flask application
CMD ["python", "app.py"]
