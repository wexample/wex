# wex vFalse

A CLI tool written in Python.

Join our community, support us, and find work at https://wexample.com 🤝❤️👨‍💻

![wex](./src/resources/images/wex.gif)

## Features

 - A strict framework for development and applications management.
 - Initialize and run Docker application.
 - Talk about your app with the AI integration.
 - Ability to execute both Python and Bash commands seamlessly, without the need for subprocesses.

## Install

### Requirements

 - Bash 5
 - Python 3.10
 - Docker 23

### Debian APT Package

    # Install dependencies
    sudo apt update
    sudo apt install gnupg2 wget -y
    
    # Add GPG key
    sudo wget -O - https://apt.wexample.com/gpg | sudo apt-key add -
    
    # Add repo
    echo "deb http://apt.wexample.com/ stable main" | sudo tee /etc/apt/sources.list.d/wexample.list
    sudo apt-get update
    
    # Install
    sudo apt install wex

Upgrading

    sudo apt update && sudo apt install --only-upgrade wex
    # Or
    wex update

### Debian from sources

    # Inside repository
    sudo cli/install

## Calling commands

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

## Services

Each service has a unique name for all addons.

## Webhook listener

A webhook listener allow you to control your server and applications remotely.

    # Start listener on port 4242
    wex app::webhook/listen 

This is existing entrypoints :

- `/status` : Return the current status of listener, useful to check availability
- `/webhook/app_name/script_name` : Execute the given script of given application

## Execution Flow

1. **Initialization**:
    - The entry point is a Bash script.
    - On invocation, the script captures the initial command and generates a unique process ID.

2. **Python Execution**:
    - The Bash script then invokes the main Python script (`__main__.py`), passing along the generated process ID and
      any additional arguments.
    - During its execution, the Python script might determine that there are subsequent Bash commands that need to be
      run. If so, it writes these commands to a temporary file.

3. **Post-Python Bash Execution**:
    - Once the Python script completes its execution, control returns to the Bash script.
    - The Bash script checks for the existence of the aforementioned temporary file.
    - If this file exists, the Bash script executes the commands contained within and then deletes the file.

## License

This project is licensed under the MIT License. For more information, please see
the [MIT License on the official Open Source Initiative (OSI) website](https://opensource.org/licenses/MIT).

