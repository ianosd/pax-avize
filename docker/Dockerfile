# Use Alpine base image
FROM python:3-alpine

# Install Python, pip, and nginx
RUN apk update && \
    apk add --no-cache python3 nginx

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy application files
COPY dist /data/www
COPY server.py /app/server.py
COPY nginx.conf /etc/nginx/nginx.conf

# Set environment variables
ENV EPAPER_HOST=localhost \
    EPAPER_PORT=8080

# Expose port
EXPOSE 80

# Start Nginx and the Python server
CMD nginx && python3 /app/server.py
#CMD nginx
