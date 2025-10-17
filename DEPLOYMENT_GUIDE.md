# CI/CD and Deployment Setup Guide

## Prerequisites

### 1. Azure VM Setup (Already Done ✅)
- VM Name: VMexam
- IP: 51.12.210.9
- OS: Ubuntu 22.04
- Size: Standard D2s v3 (2 vCPUs, 8 GiB RAM)

### 2. Required GitHub Secrets

Set up the following secrets in your GitHub repository:

```bash
# SSH Configuration
VM_SSH_PRIVATE_KEY=<your-ssh-private-key>

# Database Configuration
POSTGRES_PASSWORD=<strong-database-password>

# Security Keys
JWT_SECRET_KEY=<strong-jwt-secret-32-chars>
APP_ENCRYPTION_KEY=<strong-encryption-key-32-chars>
```

## Deployment Steps

### Step 1: VM Preparation
Run the setup script on your Azure VM:

```bash
# SSH into your VM
ssh azureuser@51.12.210.9

# Download and run the setup script
wget https://raw.githubusercontent.com/yourusername/yourrepository/main/scripts/vm-setup.sh
chmod +x vm-setup.sh
./vm-setup.sh

# Reboot the VM
sudo reboot
```

### Step 2: GitHub Repository Setup

1. **Create GitHub Repository**
   ```bash
   # Initialize git repository
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/mc101-voting-api.git
   git push -u origin main
   ```

2. **Configure Repository Secrets**
   - Go to GitHub Repository → Settings → Secrets and variables → Actions
   - Add the required secrets listed above

3. **Grant Azure IAM Access**
   - Navigate to Azure Portal → Resource Groups → [Your Resource Group]
   - Access control (IAM) → Add role assignment
   - Role: Reader
   - Assign to: Siamak.khatami@kristiania.no

### Step 3: SSH Key Setup

Generate SSH key pair for deployment:

```bash
# Generate SSH key pair
ssh-keygen -t rsa -b 4096 -C "github-actions@mc101.app" -f ~/.ssh/mc101_deploy_key

# Add public key to VM
ssh-copy-id -i ~/.ssh/mc101_deploy_key.pub azureuser@51.12.210.9

# Copy private key content for GitHub secrets
cat ~/.ssh/mc101_deploy_key
```

## CI/CD Pipeline Features

### 🏗️ Build Stage
- ✅ Python dependency installation
- ✅ Code quality checks (flake8, black, isort)
- ✅ Comprehensive test suite with coverage
- ✅ Multi-platform Docker image builds

### 🔍 Security Stage
- ✅ Container vulnerability scanning with Trivy
- ✅ SARIF security report upload
- ✅ Dependency security checks

### 🚀 Deploy Stage
- ✅ Zero-downtime deployment
- ✅ Docker image pull and update
- ✅ Health checks and validation
- ✅ Automated rollback on failure

### 📊 Monitoring Stage
- ✅ Application health verification
- ✅ Service status monitoring
- ✅ Deployment success/failure notifications

## Deployment Architecture

```
GitHub → Actions → GHCR → Azure VM
   ↓        ↓        ↓        ↓
 Code → Build → Image → Deploy
```

### Container Architecture on VM:
- **Nginx**: Reverse proxy + SSL termination
- **Voting App** (3 replicas): FastAPI application
- **PostgreSQL**: Database with persistent storage
- **Backup Cron**: Automated backup service

## Monitoring and Maintenance

### Health Checks
```bash
# Manual health check
ssh azureuser@51.12.210.9 'cd ~/mc101-app && ./health-check.sh'

# View application logs
ssh azureuser@51.12.210.9 'cd ~/mc101-app && docker-compose -f docker-compose.prod.yml logs'
```

### Backup Management
- Automated hourly PostgreSQL backups
- 7-day retention policy
- Backup location: `~/mc101-app/backups/`

### Security Features
- Fail2ban SSH protection
- UFW firewall configuration
- SSL/TLS encryption with custom certificates
- Container isolation
- Automated security updates

## Troubleshooting

### Common Issues

1. **Deployment Fails**
   ```bash
   # Check GitHub Actions logs
   # Verify SSH connectivity
   ssh azureuser@51.12.210.9 'docker ps'
   ```

2. **Application Not Responding**
   ```bash
   # Check service status
   ssh azureuser@51.12.210.9 'cd ~/mc101-app && docker-compose -f docker-compose.prod.yml ps'
   
   # Restart services
   ssh azureuser@51.12.210.9 'cd ~/mc101-app && docker-compose -f docker-compose.prod.yml restart'
   ```

3. **SSL Certificate Issues**
   ```bash
   # Regenerate certificates
   ssh azureuser@51.12.210.9 'cd ~/mc101-app && sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout nginx/ssl/nginx.key -out nginx/ssl/nginx.crt -subj "/C=NO/ST=Oslo/L=Oslo/O=MC101/CN=51.12.210.9"'
   ```

## Accessing the Application

- **Main Application**: https://51.12.210.9
- **API Documentation**: https://51.12.210.9/mc101docs
- **Health Check**: Manual via SSH or automated monitoring

## Next Steps

1. ✅ Complete VM setup using the provided script
2. ✅ Configure GitHub repository and secrets
3. ✅ Grant Azure IAM access to Siamak.khatami@kristiania.no
4. ✅ Push code to trigger CI/CD pipeline
5. ✅ Monitor deployment logs and verify application access
6. ✅ Download GitHub Actions workflow logs for documentation