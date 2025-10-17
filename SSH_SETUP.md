# SSH Key Setup for Azure VM Deployment

## Generated SSH Keys

### Public Key (Add to Azure VM)
```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC+cjGBG/CqdLsBUcEyNFsgFPboRHl7a41s6L0nKyDaQwG/Zr03T/MBK5w53Alid3ri4GzoHdA+2wlmgaRakDP0D/Y9ojo7V7yHCfaOuv/yEHZ4qg8RfUX1GLh9QZSmtzw530A+md/l7b2y9y/6NxETK1f9krz+b96llkxpkOQ2N3xs5qvtObFUQK5uqboBfJxSJMtCZu9ZzvPs5HhSd2XyCpXkYSdw8HGBJJLE5e0aMRePwyADszWOLI96fxmuTpwe+Wqwf/5o16oEgLlMwH7Cc+zP9tqmY+r0U26h+fboiG17DSEkw+l1yM532/3enx7RWN/ES3InAlv64dCKOF6ivp1HOwGR+R6tvj5gfsaodeGFs2n4sUytOeIsejCQ8XDsEYwf6cZ0W1OydhO3irKhuSNSgUXY0XSxzoSEd3KLEOTGPnZc+54BzOfQ36ueEs88sVPvkdFwoB/pS9fC5JJgA9ruy/HpNnMrqQw5CXUQNUm0KNkovUqxjc9Se+F8ZsbwBY+/KdYliyJltHOtZQOAaRoIEd6bNNps53xN75xpqso9ZVpuPsrxWlce/Ln2+NEsn+HwuTV0DRAhZc//bPztx19SEe7kn8k7acRdnAdXI1VoWZ+2xt6ejOZiPvfOjz6VG4Ey7yCRdAIBsih9+/ztI2kVNJHZLMiNd+ovYjxGdw== github-actions@mc101.app
```

### Private Key (Add to GitHub Secrets as VM_SSH_PRIVATE_KEY)
```
-----BEGIN OPENSSH PRIVATE KEY-----
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
-----END OPENSSH PRIVATE KEY-----
```

## Setup Instructions

### Step 1: Add Public Key to Azure VM
Connect to your Azure VM and add the public key:

```bash
# SSH into your Azure VM
ssh azureuser@51.12.210.9

# Create .ssh directory if it doesn't exist
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Add the public key to authorized_keys
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC+cjGBG/CqdLsBUcEyNFsgFPboRHl7a41s6L0nKyDaQwG/Zr03T/MBK5w53Alid3ri4GzoHdA+2wlmgaRakDP0D/Y9ojo7V7yHCfaOuv/yEHZ4qg8RfUX1GLh9QZSmtzw530A+md/l7b2y9y/6NxETK1f9krz+b96llkxpkOQ2N3xs5qvtObFUQK5uqboBfJxSJMtCZu9ZzvPs5HhSd2XyCpXkYSdw8HGBJJLE5e0aMRePwyADszWOLI96fxmuTpwe+Wqwf/5o16oEgLlMwH7Cc+zP9tqmY+r0U26h+fboiG17DSEkw+l1yM532/3enx7RWN/ES3InAlv64dCKOF6ivp1HOwGR+R6tvj5gfsaodeGFs2n4sUytOeIsejCQ8XDsEYwf6cZ0W1OydhO3irKhuSNSgUXY0XSxzoSEd3KLEOTGPnZc+54BzOfQ36ueEs88sVPvkdFwoB/pS9fC5JJgA9ruy/HpNnMrqQw5CXUQNUm0KNkovUqxjc9Se+F8ZsbwBY+/KdYliyJltHOtZQOAaRoIEd6bNNps53xN75xpqso9ZVpuPsrxWlce/Ln2+NEsn+HwuTV0DRAhZc//bPztx19SEe7kn8k7acRdnAdXI1VoWZ+2xt6ejOZiPvfOjz6VG4Ey7yCRdAIBsih9+/ztI2kVNJHZLMiNd+ovYjxGdw== github-actions@mc101.app" >> ~/.ssh/authorized_keys

# Set proper permissions
chmod 600 ~/.ssh/authorized_keys

# Test the connection
exit
```

### Step 2: Add Private Key to GitHub Secrets
1. Go to your GitHub repository
2. Navigate to Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `VM_SSH_PRIVATE_KEY`
5. Value: Copy the entire private key including the BEGIN and END lines
6. Click "Add secret"

### Step 3: Test SSH Connection
```bash
# Test the connection with the new key
ssh -i ~/.ssh/mc101_deploy_key azureuser@51.12.210.9
```

## Security Notes

⚠️ **Important Security Considerations:**

1. **Private Key Security**: The private key is stored in GitHub Secrets and should never be shared
2. **Key Rotation**: Consider rotating SSH keys regularly
3. **Access Control**: Only authorized GitHub Actions workflows can access the private key
4. **VM Security**: The public key allows deployment access only
5. **Monitoring**: Monitor SSH access logs on the VM for any suspicious activity

## Verification

After setup, verify the SSH configuration works:

```bash
# From your local machine
ssh -i ~/.ssh/mc101_deploy_key azureuser@51.12.210.9 "echo 'SSH connection successful!'"
```

If successful, you're ready to proceed with the GitHub repository setup and CI/CD pipeline activation.