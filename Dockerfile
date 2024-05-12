FROM python:3.12

# Disable pip version check and set Python runtime to unbuffered mode
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Create a non-root user 'djangoapp' with no password
RUN adduser --disabled-password --gecos '' djangoapp

# Ensure that all directories and files in /app are owned by 'djangoapp'
# and switch to 'djangoapp' before running any further commands
COPY --chown=djangoapp:djangoapp . /app

# Switch to 'djangoapp' to run all following commands
USER djangoapp

# Set environment variable PATH to include local bin
ENV PATH="/home/djangoapp/.local/bin:${PATH}"

# Install dependencies
RUN pip install --user -r requirements.txt

# Expose port 8000 for the application
EXPOSE 8000

# Command to start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]