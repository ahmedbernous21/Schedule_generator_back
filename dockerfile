# Use an official Python runtime as a parent image
FROM python:3.10.1

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=unilar.settings

#install psycopg dependencies
RUN apt-get update && apt-get install -y \
	build-essential \
	libpq-dev \
	&& rm -rf /var/lib/api/lists/*

# Set the working directory to /code
WORKDIR /code

ADD requirements.txt /code/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

ADD . /code/

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
