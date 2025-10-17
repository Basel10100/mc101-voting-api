# Nginx Configuration and Security Guide

This guide provides complete nginx configuration with security best practices for the Voting System application.

## Table of Contents
- [Complete nginx.conf Configuration](#complete-nginxconf-configuration)
- [Security Features Explained](#security-features-explained)
- [Testing Commands](#testing-commands)
- [Docker Integration](#docker-integration)
- [Troubleshooting](#troubleshooting)

## Complete nginx.conf Configuration

Copy and paste this complete configuration into your `nginx/nginx.conf` file:

```nginx
worker_processes auto;  # Use all available CPU cores

events {
    worker_connections 1024;  # Increase if you expect more connections
    # This is the maximum number of simultaneous connections that can be handled by a worker process
    use epoll;  # Use efficient connection method on Linux
}

http {
    # Basic security settings
    server_tokens off;  # Hide nginx version
    
    # Rate limiting zones
    limit_req_zone $binary_remote_addr zone=general:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
    limit_req_zone $binary_remote_addr zone=api:10m rate=30r/m;
    
    # Connection limiting
    limit_conn_zone $binary_remote_addr zone=perip:10m;
    limit_conn_zone $server_name zone=perserver:10m;
    
    # Security headers (will be added to all responses)
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self';" always;
    
    # Gzip compression for better performance
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    
    # Client request limits
    client_max_body_size 10M;  # Maximum request body size
    client_body_timeout 12;
    client_header_timeout 12;
    send_timeout 10;
    
    # Buffer sizes
    client_body_buffer_size 10K;
    client_header_buffer_size 1k;
    large_client_header_buffers 2 1k;

    upstream voting_app_load_balancer { 
        # Get all the instances of the voting app service and their port automatically from docker compose
        server voting_app:8000 max_fails=3 fail_timeout=30s;
        # dns resolver
        # resolver 127.0.0.11 valid=30s;
    }

    server {
        listen 80;
        server_name localhost;  # Change this to your domain name or IP if needed
        
        # Connection limits per IP
        limit_conn perip 10;  # Max 10 connections per IP
        limit_conn perserver 100;  # Max 100 connections to server
        
        # Block common malicious requests
        location ~* \.(php|asp|aspx|jsp)$ {
            return 444;  # Close connection without response
        }
        
        # Block access to hidden files
        location ~ /\. {
            deny all;
            return 404;
        }
        
        # Rate limited login endpoint
        location ~* ^/(api/)?users/(login|register) {
            limit_req zone=login burst=3 nodelay;
            limit_req_status 429;
            
            proxy_pass http://voting_app_load_balancer;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header X-Forwarded-Host $server_name;
            
            # Additional security headers for auth endpoints
            add_header X-Rate-Limit-Rule "login" always;
        }
        
        # Rate limited API endpoints
        location ~* ^/api/ {
            limit_req zone=api burst=10 nodelay;
            limit_req_status 429;
            
            proxy_pass http://voting_app_load_balancer;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header X-Forwarded-Host $server_name;
            
            # API-specific headers
            add_header X-Rate-Limit-Rule "api" always;
        }
        
        # General rate limiting for all other requests
        location / {
            limit_req zone=general burst=20 nodelay;
            limit_req_status 429;
            
            proxy_pass http://voting_app_load_balancer;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header X-Forwarded-Host $server_name;
            
            # Timeout settings
            proxy_connect_timeout 5s;
            proxy_send_timeout 10s;
            proxy_read_timeout 10s;
            
            add_header X-Rate-Limit-Rule "general" always;
        }
        
        # Custom error pages
        error_page 429 @rate_limit_exceeded;
        error_page 502 503 504 @backend_error;
        
        location @rate_limit_exceeded {
            add_header Content-Type "application/json" always;
            return 429 '{"error":"Rate limit exceeded","message":"Too many requests, please try again later"}';
        }
        
        location @backend_error {
            add_header Content-Type "application/json" always;
            return 503 '{"error":"Service temporarily unavailable","message":"Backend service is currently unavailable"}';
        }
    }
}
```

## Security Features Explained

### 1. Rate Limiting Zones

```nginx
# Rate limiting zones
limit_req_zone $binary_remote_addr zone=general:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
limit_req_zone $binary_remote_addr zone=api:10m rate=30r/m;
```

- **General Zone**: 10 requests per second per IP
- **Login Zone**: 5 requests per minute per IP (strict for authentication)
- **API Zone**: 30 requests per minute per IP

### 2. Security Headers

```nginx
# Security headers (will be added to all responses)
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self';" always;
```

### 3. Connection Limiting

```nginx
# Connection limiting
limit_conn_zone $binary_remote_addr zone=perip:10m;
limit_conn_zone $server_name zone=perserver:10m;

# In server block:
limit_conn perip 10;  # Max 10 connections per IP
limit_conn perserver 100;  # Max 100 connections to server
```

### 4. Malicious Request Blocking

```nginx
# Block common malicious requests
location ~* \.(php|asp|aspx|jsp)$ {
    return 444;  # Close connection without response
}

# Block access to hidden files
location ~ /\. {
    deny all;
    return 404;
}
```

### 5. Client Request Limits

```nginx
# Client request limits
client_max_body_size 10M;  # Maximum request body size
client_body_timeout 12;
client_header_timeout 12;
send_timeout 10;

# Buffer sizes
client_body_buffer_size 10K;
client_header_buffer_size 1k;
large_client_header_buffers 2 1k;
```

### 6. Gzip Compression

```nginx
# Gzip compression for better performance
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
```

## Testing Commands

### Test Rate Limiting

```bash
# Test general rate limiting (should see 429 errors after ~10 requests)
for i in {1..30}; do 
  curl -w "Request $i: %{http_code}\n" -o /dev/null -s http://localhost/
  sleep 0.1
done
```

```bash
# Test login rate limiting (should see 429 errors after 5 requests)
for i in {1..10}; do 
  curl -X POST -w "Login attempt $i: %{http_code}\n" -o /dev/null -s \
    -H "Content-Type: application/json" \
    -d '{"email":"test@test.com","password":"test"}' \
    http://localhost/api/users/login
  sleep 1
done
```

```bash
# Test API rate limiting
for i in {1..40}; do 
  curl -w "API request $i: %{http_code}\n" -o /dev/null -s http://localhost/api/users/
  sleep 1
done
```

### Test Security Headers

```bash
# Check security headers
curl -I http://localhost/
```

Expected headers:
```
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self';
```

### Test Malicious Request Blocking

```bash
# Test PHP file blocking (should return no response - connection closed)
curl -v http://localhost/malicious.php

# Test hidden file blocking (should return 404)
curl -v http://localhost/.env
```

## Docker Integration

### docker-compose.yml Nginx Service

```yaml
nginx:
  image: nginx:latest
  container_name: nginx_container
  ports:
    - "80:80"
    - "443:443"  # For HTTPS (when SSL is configured)
  volumes:
    - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    - ./nginx:/etc/nginx/conf.d:ro
  depends_on:
    - voting_app
  restart: unless-stopped
```

### Start with Scaling

```bash
# Start with 3 application instances behind nginx
docker-compose up --scale voting_app=3
```

### Nginx Configuration Test

```bash
# Test nginx configuration inside container
docker exec nginx_container nginx -t

# Reload nginx configuration
docker exec nginx_container nginx -s reload
```

## HTTPS/SSL Configuration (Optional)

If you want to add HTTPS support, add this server block:

```nginx
server {
    listen 443 ssl http2;
    server_name localhost;
    
    # SSL configuration
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    # SSL security headers
    add_header Strict-Transport-Security "max-age=63072000" always;
    
    # Same location blocks as HTTP server...
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name localhost;
    return 301 https://$server_name$request_uri;
}
```

## Performance Monitoring

### Check Nginx Status

```bash
# View nginx processes
docker exec nginx_container ps aux | grep nginx

# Check nginx error logs
docker logs nginx_container

# Monitor access logs in real-time
docker exec nginx_container tail -f /var/log/nginx/access.log
```

### Rate Limit Monitoring

```bash
# Monitor rate limit responses
docker exec nginx_container grep "429" /var/log/nginx/access.log | tail -10
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Configuration Test Failed

```bash
# Test configuration
docker exec nginx_container nginx -t
```

#### 2. Rate Limits Too Strict

Adjust these values in the configuration:

```nginx
# Increase rates if needed
limit_req_zone $binary_remote_addr zone=general:10m rate=20r/s;  # Increased from 10r/s
limit_req_zone $binary_remote_addr zone=api:10m rate=60r/m;      # Increased from 30r/m

# Increase burst values
limit_req zone=general burst=40 nodelay;  # Increased from 20
```

#### 3. Backend Connection Issues

```bash
# Check if backend service is running
docker-compose ps voting_app

# Test direct backend connection
curl http://localhost:8000/  # If voting_app is exposed
```

#### 4. Security Headers Causing Issues

Temporarily disable CSP to test:

```nginx
# Comment out CSP header for testing
# add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self';" always;
```

### Debug Commands

```bash
# View full nginx error log
docker exec nginx_container cat /var/log/nginx/error.log

# Check nginx configuration syntax
docker exec nginx_container nginx -T

# Monitor real-time requests
docker exec nginx_container tail -f /var/log/nginx/access.log
`` 