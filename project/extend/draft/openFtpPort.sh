
# Open 21
ufw allow 21/tcp
# Or range : ufw allow 30000:30059/tcp

# Reload (may broke ssh connexion)
ufw disable
ufw enable

# Check status
ufw status verbose

# Now, restart containers to listen port again
# You can test with :
# - On server : `nc -l -p 21`
# - From outside : nmap -p YOUR_SERVER_HOST
