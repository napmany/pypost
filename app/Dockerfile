# Use the official Python image with Python 3.12
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy pyproject.toml and poetry.lock
COPY pyproject.toml poetry.lock /app/

# Install Poetry
RUN pip install poetry

# Install dependencies
RUN poetry config virtualenvs.create false && poetry install

# Copy the rest of the application code
COPY . /app

# Expose the port
EXPOSE 8005

# Command to run the application
CMD ["uvicorn", "src.run:app", "--host", "0.0.0.0", "--port", "8005"]