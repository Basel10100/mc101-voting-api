# GitHub Repository Setup Guide

## Step-by-Step GitHub Repository Creation

### Step 1: Create GitHub Repository
1. Go to [GitHub.com](https://github.com) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Configure the repository:
   - **Repository name**: `mc101-voting-api`
   - **Description**: `MC101 Notes & Voting API - Secure microservices application with encrypted notes and voting system`
   - **Visibility**: Public (or Private if preferred)
   - **Don't initialize** with README, .gitignore, or license (we already have these)
5. Click "Create repository"

### Step 2: Connect Local Repository to GitHub
```bash
# Add the remote origin (replace USERNAME with your GitHub username)
git remote add origin https://github.com/USERNAME/mc101-voting-api.git

# Verify the remote was added
git remote -v

# Push the code to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Configure GitHub Secrets
Navigate to your repository → Settings → Secrets and variables → Actions

Add the following secrets:

#### Required Secrets:
```
VM_SSH_PRIVATE_KEY
-----BEGIN OPENSSH PRIVATE KEY-----
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
-----END OPENSSH PRIVATE KEY-----
```

```
POSTGRES_PASSWORD=-ERtkUSJjAgNin1LfeyeOQ
```

```
JWT_SECRET_KEY=h3ym_MziX0s4hvNH8v6ZaInlPc-JkC3dWsqxPWXE6pA
```

```
APP_ENCRYPTION_KEY=P_bnwCzKdNWxuZ0KaWUDZoln1c9LaZTtjWHJHqwh4fQ
```

### Step 4: Add Collaborator
1. In your repository, go to Settings → Manage access
2. Click "Invite a collaborator"
3. Enter: `Siamak.khatami@kristiania.no`
4. Select role: "Write" (allows viewing code, issues, and pull requests)
5. Send invitation

### Step 5: Setup Azure VM SSH Access
Before the CI/CD pipeline can deploy, add the SSH public key to your Azure VM:

```bash
# SSH into your Azure VM
ssh azureuser@51.12.210.9

# Add the public key to authorized_keys
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC+cjGBG/CqdLsBUcEyNFsgFPboRHl7a41s6L0nKyDaQwG/Zr03T/MBK5w53Alid3ri4GzoHdA+2wlmgaRakDP0D/Y9ojo7V7yHCfaOuv/yEHZ4qg8RfUX1GLh9QZSmtzw530A+md/l7b2y9y/6NxETK1f9krz+b96llkxpkOQ2N3xs5qvtObFUQK5uqboBfJxSJMtCZu9ZzvPs5HhSd2XyCpXkYSdw8HGBJJLE5e0aMRePwyADszWOLI96fxmuTpwe+Wqwf/5o16oEgLlMwH7Cc+zP9tqmY+r0U26h+fboiG17DSEkw+l1yM532/3enx7RWN/ES3InAlv64dCKOF6ivp1HOwGR+R6tvj5gfsaodeGFs2n4sUytOeIsejCQ8XDsEYwf6cZ0W1OydhO3irKhuSNSgUXY0XSxzoSEd3KLEOTGPnZc+54BzOfQ36ueEs88sVPvkdFwoB/pS9fC5JJgA9ruy/HpNnMrqQw5CXUQNUm0KNkovUqxjc9Se+F8ZsbwBY+/KdYliyJltHOtZQOAaRoIEd6bNNps53xN75xpqso9ZVpuPsrxWlce/Ln2+NEsn+HwuTV0DRAhZc//bPztx19SEe7kn8k7acRdnAdXI1VoWZ+2xt6ejOZiPvfOjz6VG4Ey7yCRdAIBsih9+/ztI2kVNJHZLMiNd+ovYjxGdw== github-actions@mc101.app" >> ~/.ssh/authorized_keys

# Set proper permissions
chmod 600 ~/.ssh/authorized_keys

# Run the VM setup script
wget https://raw.githubusercontent.com/USERNAME/mc101-voting-api/main/scripts/vm-setup.sh
chmod +x vm-setup.sh
./vm-setup.sh
```

### Step 6: Trigger CI/CD Pipeline
Once everything is set up, any push to the `main` branch will trigger the CI/CD pipeline:

```bash
# Make a small change to trigger deployment
echo "# CI/CD Pipeline Active" >> README.md
git add README.md
git commit -m "Activate CI/CD pipeline"
git push origin main
```

### Step 7: Monitor Deployment
1. Go to your GitHub repository
2. Click on "Actions" tab
3. Monitor the workflow progress
4. Download workflow logs for your report

### Step 8: Verify Deployment
After successful deployment, verify your application:

- **Application**: https://51.12.210.9
- **API Docs**: https://51.12.210.9/mc101docs
- **Health Check**: https://51.12.210.9/health

## Repository Structure
```
mc101-voting-api/
├── .github/workflows/
│   └── ci-cd.yml                 # Main CI/CD pipeline
├── api/                          # API modules
├── nginx/                        # Nginx configuration
├── scripts/                      # Deployment scripts
├── tests/                        # Test suite
├── utils/                        # Utility modules
├── docker-compose.yml            # Local development
├── Dockerfile                    # Main app container
├── requirements.txt              # Python dependencies
├── MC101_Project_Report.md       # Final project report
├── AZURE_LOAD_TESTING.md         # Load testing guide
└── README.md                     # Project documentation
```

## Next Steps

1. ✅ Create GitHub repository
2. ✅ Configure secrets
3. ✅ Add collaborator: `Siamak.khatami@kristiania.no`
4. ✅ Setup VM SSH access
5. ✅ Push code and trigger CI/CD
6. ⏳ Monitor deployment
7. ⏳ Setup Azure Load Testing
8. ⏳ Download workflow logs for report

## Troubleshooting

### Common Issues:
1. **SSH Connection Failed**: Verify public key is added to VM's authorized_keys
2. **Secrets Not Found**: Ensure all 4 secrets are configured in GitHub
3. **Deployment Timeout**: Check VM resources and Docker service status
4. **Health Check Failed**: Verify application is running and accessible

### Support Commands:
```bash
# Check VM status
ssh azureuser@51.12.210.9 'docker ps'

# View application logs
ssh azureuser@51.12.210.9 'cd ~/mc101-app && docker-compose logs'

# Restart services
ssh azureuser@51.12.210.9 'cd ~/mc101-app && docker-compose restart'
```