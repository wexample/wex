if [[ $- != *i* ]]; then
    # Trigger error on failing
    set -e
    # Ensure the script fails if any command in a pipeline fails
    set -o pipefail
fi