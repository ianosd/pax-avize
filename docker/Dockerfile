FROM python:3-slim

# Install nginx and Firebird client library
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        nginx \
        libfbclient2 \
        && apt-get clean

WORKDIR /app
COPY backend/requirements.txt /app/
RUN pip install -r requirements.txt

# Copy application files
COPY frontend/dist /data/www
COPY backend/*.py /app/
COPY docker/nginx.conf /etc/nginx/nginx.conf

# Set environment variables
ENV EPAPER_HOST=localhost \
    EPAPER_PORT=8080 \
    EPAPER_DATA=/app/data

# Expose port
EXPOSE 80

# Start Nginx and the Python server
CMD nginx && python3 /app/server.py
#CMD nginx
