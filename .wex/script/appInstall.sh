
_wexMessage "Install pip requirements"

wex app::app/exec -c="cd /var/www/html && sudo pip-compile requirements.in"
wex app::app/exec -c="cd /var/www/html && sudo pip install -r requirements.txt"