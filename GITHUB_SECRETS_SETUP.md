# GitHub Secrets Configuration Guide

## Required GitHub Repository Secrets

### 1. SSH Configuration
```
Name: VM_SSH_PRIVATE_KEY
Value: [Generated SSH private key - see below]
Description: SSH private key for deployment to Azure VM
```

### 2. Database Configuration
```
Name: POSTGRES_PASSWORD
Value: -ERtkUSJjAgNin1LfeyeOQ
Description: PostgreSQL database password
```

### 3. Security Keys
```
Name: JWT_SECRET_KEY
Value: h3ym_MziX0s4hvNH8v6ZaInlPc-JkC3dWsqxPWXE6pA
Description: JWT token signing secret
```

```
Name: APP_ENCRYPTION_KEY
Value: P_bnwCzKdNWxuZ0KaWUDZoln1c9LaZTtjWHJHqwh4fQ
Description: Application-level encryption key for notes
```

## Setting up GitHub Secrets

### Step 1: Navigate to Repository Settings
1. Go to your GitHub repository
2. Click on **Settings** tab
3. In the left sidebar, click **Secrets and variables** → **Actions**

### Step 2: Add Each Secret
For each secret above:
1. Click **New repository secret**
2. Enter the **Name** exactly as shown
3. Paste the **Value**
4. Click **Add secret**

### Step 3: SSH Key Setup
See the SSH key generation instructions in the deployment guide.

## Environment Variables for Local Development

The following variables are already configured in your `.env` file:

```bash
# Database
POSTGRES_DB=voting_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=-ERtkUSJjAgNin1LfeyeOQ
POSTGRES_HOST=voting_db
POSTGRES_PORT_IN_DOCKER=5432
POSTGRES_PORT_ON_MACHINE=5432

# JWT
JWT_SECRET_KEY=h3ym_MziX0s4hvNH8v6ZaInlPc-JkC3dWsqxPWXE6pA
JWT_ALGORITHM=HS256
JWT_EXPIRATION_TIME=60

# Encryption
APP_ENCRYPTION_KEY=P_bnwCzKdNWxuZ0KaWUDZoln1c9LaZTtjWHJHqwh4fQ
```

## Security Notes

⚠️ **Important Security Considerations:**

1. **Never commit secrets to Git** - The `.env` file is already in `.gitignore`
2. **Rotate keys regularly** - These keys should be changed periodically
3. **Use strong passwords** - All generated secrets use cryptographically secure random generation
4. **Limit access** - Only grant repository access to trusted collaborators
5. **Monitor usage** - Regularly check GitHub Actions logs for any suspicious activity

## Verification

After setting up the secrets, you can verify they're configured correctly by:

1. Going to your repository Settings → Secrets and variables → Actions
2. You should see 4 secrets listed:
   - `VM_SSH_PRIVATE_KEY`
   - `POSTGRES_PASSWORD`
   - `JWT_SECRET_KEY`
   - `APP_ENCRYPTION_KEY`

## Next Steps

1. ✅ Configure GitHub secrets (above)
2. ⏳ Generate and configure SSH keys
3. ⏳ Grant Azure IAM access to `Siamak.khatami@kristiania.no`
4. ⏳ Push code to GitHub to trigger CI/CD pipeline