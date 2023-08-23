# wex v5.0.0-beta.41+build.20230822134237

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

## Calling command
    
    # Basic call in core addons folders
    wex core::logo/show

    # User defined command, stored in home directory
    wex ~local_command_group/local_command_name

    # Custom command inside an app
    wex .custom_command_group/custom_command_name

    # Service command
    wex @service_name::custom_command_group/command_name

## Addons

Commands and services are organised in several "addons".

### Services

Each service has a unique name for all addons.

## License

This project is licensed under the MIT License. For more information, please see the [MIT License on the official Open Source Initiative (OSI) website](https://opensource.org/licenses/MIT).

