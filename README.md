# wex v5.0.0-beta.28+build.20230611121916

A single entrypoint to execute custom bash scripts, and run Docker application on several environments. See description for more info.

Join our community, support us, and find work at https://wexample.com 🤝❤️👨‍💻

## Install

### Debian
    # Install dependencies
    sudo apt install gnupg2 wget -y
    
    # Add GPG key
    sudo wget -O - https://apt.wexample.com/gpg | sudo apt-key add -
    
    # Add repo
    echo "deb http://apt.wexample.com/ beta main" | sudo tee /etc/apt/sources.list.d/wexample.list
    sudo apt-get update
    
    # Install
    sudo apt install wex

## License

This project is licensed under the MIT License. For more information, please see the [MIT License on the official Open Source Initiative (OSI) website](https://opensource.org/licenses/MIT).

## Create a new version

- Once new features are ready to deploy :


    # Update version number
    wex core::version/build
    # ... check changes then ...
    # Commit and tag new version
    wex core::version/build -ok
    # Push when ready to deploy
    git push

