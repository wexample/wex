#!/bin/bash

wexample_dir="$HOME/"
# TODO Use another, and more stable hosting service.
wexample_url="https://network.wexample.com"

RED='\033[1;91m'
WHITE='\033[0;30m'
NC='\033[0m'

# Continued from above example
echo -e "${RED}"

echo "                        .";
echo "                   .-=======-.";
echo "               .-=======+=======-.";
echo "           .-===========++==========-.";
echo "        .-==========!|==+++|!==========-.";
echo "        |++=======?  |==!++|  ?=========|";
echo "        |++++==|     |?   ^|     |======|";
echo "        |++++++|                 |======|";
echo "        |++++++|                 |======|";
echo "        |++++++|                 |======|";
echo "        |++++++++ _    _!_    _ ========|";
echo "        ?-+++++++++++.=====.===========-?";
echo "           ?-+++++++++++============-?";
echo "               ?-++++++++=======-?";
echo "                   ?-++++===-?";
echo "                        +";

echo -e "${NC}";

echo "                                          _";
echo "                                         | |";
echo "  __      _______  ____ _ _ __ ___  _ __ | | ___";
echo "  \ \ /\ / / _ \ \/ / _\` | '_ \` _ \| '_ \| |/ _ \\";
echo "   \ V  V /  __/>  < (_| | | | | | | |_) | |  __/";
echo "    \_/\_/ \___/_/\_\__,_|_| |_| |_| .__/|_|\___|";
echo "     http://network.wexample.com   | |";
echo "     # Scripts recipe              |_|";

# TODO Not tested
. "wexample.sh"

echo "Starting wexample recipe : Run wexample script ...............";

# Use standard method to load script
wexample_load_recipe $1

echo "Wexample script complete .....................................";
