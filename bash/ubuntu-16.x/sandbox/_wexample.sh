#!/usr/bin/env bash

# Load given recipe
wexample_load_recipe () {
  script_id=$1
  file_name="wexample-$script_id.sh"
  # Load the file and
  # convert windows lines breaks
  echo "Loading $file_name..."
  curl $wexample_url/node/$script_id/recipe/raw | tr -d "\015" > ${file_name}
  # Run
  echo "Exectue $file_name"
  bash ${file_name}
  # Destroy file
  echo "Remove $file_name"
  rm ${file_name}
}

