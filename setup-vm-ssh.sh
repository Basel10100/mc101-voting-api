#!/bin/bash

# This script will setup SSH access to your Azure VM
# Run this on your Azure VM after SSH'ing into it

echo "🔧 Setting up SSH access for GitHub Actions deployment..."

# Create .ssh directory if it doesn't exist
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Add the GitHub Actions public key to authorized_keys
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC+cjGBG/CqdLsBUcEyNFsgFPboRHl7a41s6L0nKyDaQwG/Zr03T/MBK5w53Alid3ri4GzoHdA+2wlmgaRakDP0D/Y9ojo7V7yHCfaOuv/yEHZ4qg8RfUX1GLh9QZSmtzw530A+md/l7b2y9y/6NxETK1f9krz+b96llkxpkOQ2N3xs5qvtObFUQK5uqboBfJxSJMtCZu9ZzvPs5HhSd2XyCpXkYSdw8HGBJJLE5e0aMRePwyADszWOLI96fxmuTpwe+Wqwf/5o16oEgLlMwH7Cc+zP9tqmY+r0U26h+fboiG17DSEkw+l1yM532/3enx7RWN/ES3InAlv64dCKOF6ivp1HOwGR+R6tvj5gfsaodeGFs2n4sUytOeIsejCQ8XDsEYwf6cZ0W1OydhO3irKhuSNSgUXY0XSxzoSEd3KLEOTGPnZc+54BzOfQ36ueEs88sVPvkdFwoB/pS9fC5JJgA9ruy/HpNnMrqQw5CXUQNUm0KNkovUqxjc9Se+F8ZsbwBY+/KdYliyJltHOtZQOAaRoIEd6bNNps53xN75xpqso9ZVpuPsrxWlce/Ln2+NEsn+HwuTV0DRAhZc//bPztx19SEe7kn8k7acRdnAdXI1VoWZ+2xt6ejOZiPvfOjz6VG4Ey7yCRdAIBsih9+/ztI2kVNJHZLMiNd+ovYjxGdw== github-actions@mc101.app" >> ~/.ssh/authorized_keys

# Set proper permissions
chmod 600 ~/.ssh/authorized_keys

echo "✅ SSH key added successfully!"
echo "📊 Current authorized keys:"
cat ~/.ssh/authorized_keys

echo ""
echo "🎉 SSH setup complete! GitHub Actions can now deploy to this VM."