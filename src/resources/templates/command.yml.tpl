webhook: false
help: Description
scripts:
  - echo "Inline bash script example"

  - title: Bash outside container but with running app
    app_should_run: true
    script: echo "Inline bash script outside running app"

  - title: Bash inside container
    context: container
    container_name: php
    script: echo "Inline bash script inside container of a running app"

  - title: Running bash file
    type: bash-file
    file: .wex/bash/file.sh

  - title: Inline python
    type: python
    script: print('Python script')

  - title: File in python
    type: python-file
    file: .wex/python/file.py