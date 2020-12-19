FROM python:3.8-buster

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install production packages
RUN pip install --no-cache-dir gunicorn psycopg2

# Install app dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy app
COPY . /app

RUN useradd -u 1001 appuser
USER appuser

# The entrypoint is used to migrate upon start
ENTRYPOINT ["/app/entrypoint.sh"]

# By default launch gunicorn on port 8000
CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:8000", "whitelink.wsgi"]