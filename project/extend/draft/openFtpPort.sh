
# Open 21
ufw allow 21/tcp

# Reload (may broke ssh connexion)
ufw disable
ufw enable

# Now, restart containers to listen port again
# You can test with :
# - On server : `nc -l -p 21`
# - From outside : nmap -p YOUR_SERVER_HOST
