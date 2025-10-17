## Manual VM SSH Setup Commands

Run these commands in your terminal to setup SSH access:

```bash
# 1. SSH into your Azure VM (you'll need to authenticate normally first)
ssh azureuser@51.12.210.9

# 2. Once connected to the VM, run these commands:
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# 3. Add the GitHub Actions public key
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC+cjGBG/CqdLsBUcEyNFsgFPboRHl7a41s6L0nKyDaQwG/Zr03T/MBK5w53Alid3ri4GzoHdA+2wlmgaRakDP0D/Y9ojo7V7yHCfaOuv/yEHZ4qg8RfUX1GLh9QZSmtzw530A+md/l7b2y9y/6NxETK1f9krz+b96llkxpkOQ2N3xs5qvtObFUQK5uqboBfJxSJMtCZu9ZzvPs5HhSd2XyCpXkYSdw8HGBJJLE5e0aMRePwyADszWOLI96fxmuTpwe+Wqwf/5o16oEgLlMwH7Cc+zP9tqmY+r0U26h+fboiG17DSEkw+l1yM532/3enx7RWN/ES3InAlv64dCKOF6ivp1HOwGR+R6tvj5gfsaodeGFs2n4sUytOeIsejCQ8XDsEYwf6cZ0W1OydhO3irKhuSNSgUXY0XSxzoSEd3KLEOTGPnZc+54BzOfQ36ueEs88sVPvkdFwoB/pS9fC5JJgA9ruy/HpNnMrqQw5CXUQNUm0KNkovUqxjc9Se+F8ZsbwBY+/KdYliyJltHOtZQOAaRoIEd6bNNps53xN75xpqso9ZVpuPsrxWlce/Ln2+NEsn+HwuTV0DRAhZc//bPztx19SEe7kn8k7acRdnAdXI1VoWZ+2xt6ejOZiPvfOjz6VG4Ey7yCRdAIBsih9+/ztI2kVNJHZLMiNd+ovYjxGdw== github-actions@mc101.app" >> ~/.ssh/authorized_keys

# 4. Set proper permissions
chmod 600 ~/.ssh/authorized_keys

# 5. Verify the key was added
echo "Authorized keys:"
cat ~/.ssh/authorized_keys

# 6. Exit the VM
exit
```

After you run these commands, let me know and I'll continue with pushing the code!