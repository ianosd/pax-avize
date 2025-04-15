# Use Alpine base image
FROM python:3-alpine

# Install Python, pip, and nginx
RUN apk update && \
    apk add --no-cache python3 nginx

WORKDIR /app
COPY backend/requirements.txt /app/
RUN pip install -r requirements.txt

# Copy application files
COPY frontend/dist /data/www
COPY backend/*.py /app/
COPY docker/nginx.conf /etc/nginx/nginx.conf

# Set environment variables
ENV EPAPER_HOST=localhost \
    EPAPER_PORT=8080

# Expose port
EXPOSE 80

# Start Nginx and the Python server
CMD nginx && python3 /app/server.py
#CMD nginx
