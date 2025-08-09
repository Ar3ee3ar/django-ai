# Stage 1 : Base build stage
# Use the official Python runtime image
FROM python:3.9-alpine3.19 AS builder

# Update apk packages to fix vulnerabilities
RUN apk update && apk upgrade

# Create the app directory
RUN mkdir /app

# Define work directory
WORKDIR /app

# Set environment variable
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYCODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Upgrade pip
RUN pip install --upgrade pip

# Copy the Django project and install dependencies
COPY requirements.txt /app/

# run this command to install all dependencies
RUN pip install --no-cache-dir -r requirements.txt

# stage2 : production stage
FROM python:3.9-alpine3.19

# Security best practice: running app as a non-root user inside a container
# /app directory is prepared for application files and appuser will have the necessary permissions to access and modify them 
# install shadow for useradd command
# Create a new system user named appuser -m (create home directory for the user) -r (make it a system account)
# create new directory
# change ownership of /app (and everything inside to appuser user)
RUN apk add --no-cache shadow && \
    useradd -m -r appuser && \
    mkdir /app && \
    chown -R appuser /app

# create the appropriate directories
# ENV HOME=/home/app
# ENV APP_HOME=/home/app/web
# RUN mkdir $APP_HOME
# RUN mkdir /app/static
# RUN mkdir $APP_HOME/mediafiles

# Define work directory
WORKDIR /app

# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy the django project to the container
# COPY . /app/
COPY --chown=appuser:appuser . .
COPY --chown=appuser:appuser entrypoint.sh /app/entrypoint.sh

# Set environment variable
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYCODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Switch to non-root user
USER appuser

# Expose the django port
EXPOSE 8000

# Run Django's development server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# RUN python manage.py makemigrations 
# RUN python manage.py migrate 
# RUN python manage.py collectstatic --noinput
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "mysite.wsgi:application"]
ENTRYPOINT [ "/app/entrypoint.sh" ]