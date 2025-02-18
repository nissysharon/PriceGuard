# Use an official slim Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /code

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Optionally, set PYTHONPATH so that /code is searched for modules
ENV PYTHONPATH=/code

# Expose port 8000 (optional, for documentation purposes)
EXPOSE 8000

# Command to run the Uvicorn server, pointing to app/main.py's "app" object
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
