
_wexMessage "Install pip requirements"

wex app::app/exec -c="cd /opt/wex && sudo pip-compile requirements.in && sudo pip install -r requirements.txt"