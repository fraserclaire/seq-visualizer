### Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements to the container
COPY app.py /app/
COPY static /app/static
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Automatically open the web browser when the container runs
CMD ["sh", "-c", "python app.py & sleep 2 && xdg-open http://localhost:5000 && wait"]
