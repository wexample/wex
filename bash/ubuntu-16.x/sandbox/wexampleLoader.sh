#!/bin/bash

wexample_dir="$HOME/"
# TODO Use another, and more stable hosting service.
wexample_url="https://network.wexample.com"



# TODO Not tested
. "../_wexample.sh"

echo "Starting wexample recipe : Run wexample script ...............";

# Use standard method to load script
wexample_load_recipe $1

echo "Wexample script complete .....................................";
