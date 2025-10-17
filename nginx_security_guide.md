# Nginx Security Configuration Guide

This document explains the security practices implemented in the nginx configuration for the Voting System application.

## Security Measures Implemented

### 1. Rate Limiting

#### Rate Limiting Zones
- **General Zone**: 10 requests per second per IP
  - Applied to: All general application requests
  - Burst: 20 requests (allows temporary spikes)
  
- **Login Zone**: 5 requests per minute per IP
  - Applied to: Login and registration endpoints
  - Burst: 3 requests (strict limit for auth attempts)
  
- **API Zone**: 30 requests per minute per IP
  - Applied to: All API endpoints
  - Burst: 10 requests (moderate limit for API calls)

#### Rate Limiting Benefits
- Prevents brute force attacks on login endpoints
- Protects against API abuse and DoS attacks
- Maintains service availability under high load

### 2. Connection Limiting

- **Per IP**: Maximum 10 concurrent connections per IP address
- **Per Server**: Maximum 100 concurrent connections to the server
- Prevents connection flooding attacks

### 3. Security Headers

#### Standard Security Headers
- `X-Frame-Options: SAMEORIGIN` - Prevents clickjacking attacks
- `X-Content-Type-Options: nosniff` - Prevents MIME type sniffing
- `X-XSS-Protection: 1; mode=block` - Enables XSS filtering
- `Referrer-Policy: strict-origin-when-cross-origin` - Controls referrer information

#### Content Security Policy (CSP)
```
default-src 'self'; 
script-src 'self' 'unsafe-inline'; 
style-src 'self' 'unsafe-inline'; 
img-src 'self' data:; 
font-src 'self';
```
- Prevents XSS attacks by controlling resource loading
- Allows only trusted sources for scripts, styles, and other resources

### 4. Request Filtering

#### Blocked File Types
- Blocks requests to PHP, ASP, ASPX, JSP files
- Returns 444 (connection closed) for these requests
- Prevents execution of potentially malicious scripts

#### Hidden Files Protection
- Blocks access to files starting with `.` (dot files)
- Protects configuration files, git repositories, etc.
- Returns 404 for these requests

### 5. Server Hardening

#### Information Disclosure Prevention
- `server_tokens off` - Hides nginx version in responses
- Reduces information available to attackers

#### Optimized Worker Configuration
- `worker_processes auto` - Uses all available CPU cores
- `use epoll` - Efficient connection handling on Linux

### 6. Request Limits

#### Body and Header Limits
- `client_max_body_size: 10M` - Maximum request body size
- `client_body_timeout: 12s` - Body read timeout
- `client_header_timeout: 12s` - Header read timeout
- `send_timeout: 10s` - Response send timeout

#### Buffer Limits
- `client_body_buffer_size: 10K`
- `client_header_buffer_size: 1K`
- `large_client_header_buffers: 2 1K`

### 7. Performance & Security Optimizations

#### Gzip Compression
- Reduces bandwidth usage
- Improves page load times
- Configured for common web content types

#### Proxy Settings
- Proper header forwarding for backend services
- Timeout configurations to prevent hanging connections
- Real IP forwarding for accurate logging

### 8. Custom Error Handling

#### Rate Limit Exceeded (429)
```json
{
  "error": "Rate limit exceeded",
  "message": "Too many requests, please try again later"
}
```

#### Backend Errors (502, 503, 504)
```json
{
  "error": "Service temporarily unavailable",
  "message": "Backend service is currently unavailable"
}
```

## Testing Rate Limiting

### Test General Rate Limiting
```bash
# Send requests rapidly to test general rate limiting
for i in {1..30}; do curl -w "%{http_code}\n" -o /dev/null -s http://localhost/; done
```

### Test Login Rate Limiting
```bash
# Test login endpoint rate limiting
for i in {1..10}; do curl -X POST -w "%{http_code}\n" -o /dev/null -s http://localhost/api/users/login; done
```

### Test API Rate Limiting
```bash
# Test API endpoint rate limiting
for i in {1..40}; do curl -w "%{http_code}\n" -o /dev/null -s http://localhost/api/users/; done
```

## Monitoring and Logging

### Rate Limit Headers
Each response includes a custom header indicating which rate limit rule was applied:
- `X-Rate-Limit-Rule: general`
- `X-Rate-Limit-Rule: login`
- `X-Rate-Limit-Rule: api`

### Log Analysis
Monitor nginx access logs for:
- 429 status codes (rate limit exceeded)
- Unusual request patterns
- Blocked malicious requests (444 status codes)

## Advanced Security Considerations

### Additional Measures to Consider
1. **IP Whitelisting**: For admin endpoints
2. **Geographic Blocking**: Block requests from specific countries
3. **SSL/TLS**: Upgrade to HTTPS with proper certificates
4. **ModSecurity**: Web Application Firewall (WAF) integration
5. **Fail2ban**: Automatic IP blocking based on log patterns

### Configuration Tuning
- Adjust rate limits based on actual usage patterns
- Monitor performance impact of security measures
- Regularly review and update security headers
- Keep nginx updated to latest stable version

## Troubleshooting

### Common Issues
1. **Legitimate users getting rate limited**: Increase burst values or adjust rates
2. **Backend connection issues**: Check proxy timeout settings
3. **Security headers conflicts**: Review CSP policy for your specific needs

### Debug Commands
```bash
# Test nginx configuration
nginx -t

# Reload nginx configuration
nginx -s reload

# View nginx error logs
tail -f /var/log/nginx/error.log
```

## Security Best Practices Summary

**Implemented**
- Rate limiting (3 zones)
- Connection limiting
- Security headers
- Request filtering
- Server hardening
- Custom error pages

**Recommended Next Steps**
- Implement HTTPS/SSL
- Add monitoring and alerting
- Regular security audits
- Update security policies based on threat landscape

This configuration provides a solid foundation for securing your voting application while maintaining good performance and user experience.