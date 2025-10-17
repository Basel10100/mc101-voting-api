#!/bin/bash

# Setup script for VM SSH access and deployment validation
# Run this script locally after SSH key is properly configured

VM_HOST="51.12.210.9"
VM_USER="azureuser"

echo "🔧 Setting up VM SSH access and deployment validation..."

# Test SSH connection
echo "Testing SSH connection to $VM_USER@$VM_HOST..."
ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no $VM_USER@$VM_HOST "echo 'SSH connection successful!'"

if [ $? -eq 0 ]; then
    echo "✅ SSH connection successful!"
    
    # Install Docker if not present
    echo "Installing Docker..."
    ssh $VM_USER@$VM_HOST "
        sudo apt update -y
        sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
        echo \"deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \$(lsb_release -cs) stable\" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
        sudo apt update -y
        sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
        sudo systemctl start docker
        sudo systemctl enable docker
        sudo usermod -aG docker \$USER
    "
    
    # Create deployment directory
    echo "Creating deployment directory..."
    ssh $VM_USER@$VM_HOST "mkdir -p ~/mc101-deployment"
    
    # Test Docker
    echo "Testing Docker installation..."
    ssh $VM_USER@$VM_HOST "sudo docker --version && sudo docker-compose --version"
    
    echo "✅ VM setup complete!"
    echo "🚀 You can now trigger the GitHub Actions deployment pipeline"
    echo "📱 Check: https://github.com/Basel10100/mc101-voting-api/actions"
    
else
    echo "❌ SSH connection failed!"
    echo "Please ensure:"
    echo "1. SSH key is properly configured in Azure VM"
    echo "2. Security group allows SSH (port 22)"
    echo "3. VM is running"
    echo ""
    echo "To configure SSH key manually:"
    echo "1. Go to Azure Portal -> Virtual Machine VMexam"
    echo "2. Select 'Reset password' from left menu"
    echo "3. Choose 'Reset SSH public key'"
    echo "4. Use the public key from GitHub secrets"
fi