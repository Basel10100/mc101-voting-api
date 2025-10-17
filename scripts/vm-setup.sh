#!/bin/bash

# MC101 Azure VM Setup Script
# This script prepares an Ubuntu VM for the MC101 application deployment

set -e

echo "🚀 MC101 Azure VM Setup Script"
echo "==============================="

# Update system packages
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install essential tools
echo "🔧 Installing essential tools..."
sudo apt install -y curl wget git unzip software-properties-common

# Install Docker
echo "🐳 Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    sudo systemctl enable docker
    sudo systemctl start docker
    rm get-docker.sh
    echo "✅ Docker installed successfully"
else
    echo "✅ Docker already installed"
fi

# Install Docker Compose
echo "📦 Installing Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo "✅ Docker Compose installed successfully"
else
    echo "✅ Docker Compose already installed"
fi

# Configure firewall
echo "🔒 Configuring firewall..."
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable

# Create application directory
echo "📁 Creating application directory..."
mkdir -p ~/mc101-app
cd ~/mc101-app

# Generate SSL certificates (self-signed for development)
echo "🔑 Generating SSL certificates..."
mkdir -p nginx/ssl
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout nginx/ssl/nginx.key \
    -out nginx/ssl/nginx.crt \
    -subj "/C=NO/ST=Oslo/L=Oslo/O=MC101/CN=51.12.210.9"

# Set proper permissions
sudo chown -R $USER:$USER nginx/ssl
chmod 600 nginx/ssl/nginx.key
chmod 644 nginx/ssl/nginx.crt

# Install monitoring tools
echo "📊 Installing monitoring tools..."
sudo apt install -y htop iotop nethogs

# Setup log rotation
echo "📝 Setting up log rotation..."
sudo tee /etc/logrotate.d/mc101 << EOF
/home/$USER/mc101-app/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0644 $USER $USER
}
EOF

# Create systemd service for application monitoring
echo "🔄 Creating systemd service..."
sudo tee /etc/systemd/system/mc101-monitor.service << EOF
[Unit]
Description=MC101 Application Monitor
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
User=$USER
WorkingDirectory=/home/$USER/mc101-app
ExecStart=/usr/local/bin/docker-compose -f docker-compose.prod.yml ps
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable mc101-monitor.service

# Setup backup directory with proper permissions
echo "💾 Setting up backup directory..."
mkdir -p ~/mc101-app/backups
chmod 755 ~/mc101-app/backups

# Install additional security tools
echo "🛡️ Installing security tools..."
sudo apt install -y fail2ban

# Configure fail2ban for SSH protection
sudo tee /etc/fail2ban/jail.local << EOF
[DEFAULT]
bantime = 1h
findtime = 10m
maxretry = 5

[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log
EOF

sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Setup automated security updates
echo "🔄 Configuring automatic security updates..."
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades

# Create health check script
echo "🏥 Creating health check script..."
tee ~/mc101-app/health-check.sh << 'EOF'
#!/bin/bash

echo "🏥 MC101 Application Health Check"
echo "================================="

# Check Docker services
echo "🐳 Docker Services Status:"
docker-compose -f docker-compose.prod.yml ps

echo ""
echo "📊 System Resources:"
echo "CPU Usage: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)%"
echo "Memory Usage: $(free | grep Mem | awk '{printf("%.1f%%", $3/$2 * 100.0)}')"
echo "Disk Usage: $(df -h / | awk 'NR==2{print $5}')"

echo ""
echo "🌐 Application Status:"
if curl -k -f https://localhost/ > /dev/null 2>&1; then
    echo "✅ Application is responding"
else
    echo "❌ Application is not responding"
fi

echo ""
echo "📝 Recent Logs:"
docker-compose -f docker-compose.prod.yml logs --tail=10
EOF

chmod +x ~/mc101-app/health-check.sh

# Setup crontab for health checks
echo "⏰ Setting up health check cron job..."
(crontab -l 2>/dev/null; echo "*/5 * * * * /home/$USER/mc101-app/health-check.sh >> /home/$USER/mc101-app/health-check.log 2>&1") | crontab -

echo ""
echo "✅ VM Setup Complete!"
echo "====================="
echo "Next steps:"
echo "1. Reboot the VM to ensure all changes take effect"
echo "2. Configure GitHub Secrets with the following:"
echo "   - VM_SSH_PRIVATE_KEY: Your SSH private key"
echo "   - POSTGRES_PASSWORD: Database password"
echo "   - JWT_SECRET_KEY: JWT signing key"
echo "   - APP_ENCRYPTION_KEY: Application encryption key"
echo "3. Push your code to GitHub to trigger the CI/CD pipeline"
echo ""
echo "🌐 Your application will be available at: https://51.12.210.9"
echo "📚 API documentation: https://51.12.210.9/mc101docs"