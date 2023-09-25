
if [[ $UID -ne 0 ]]; then
    echo "Installation should run in sudo."
    exit 1
fi