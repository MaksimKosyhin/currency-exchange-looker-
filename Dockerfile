# Stage 1: Builder
FROM python:3-slim-buster AS builder

# Set the working directory inside the container
WORKDIR /currency-exchange-looker

# Create and activate a virtual environment
RUN python3 -m venv venv
ENV VIRTUAL_ENV=/currency-exchange-looker/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Stage 2: Runner
FROM python:3-slim-buster AS runner

# Set the working directory inside the container
WORKDIR /currency-exchange-looker

# Copy the virtual environment from the builder stage
COPY --from=builder /currency-exchange-looker/venv venv

# Copy the application files and the necessary additional files
COPY app.py app.py
COPY updater.py updater.py
COPY service-account.json service-account.json
COPY .env .env

# Copy the templates directory (assuming it contains HTML templates)
COPY templates/ templates/

# Set environment variables for the virtual environment and Flask
ENV VIRTUAL_ENV=/currency-exchange-looker/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV FLASK_APP=app.py

# Expose the Flask default port 5000
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]

