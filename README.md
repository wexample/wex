### APT Deployment scenario

- A new version is ready to deploy and tested with the CI
- On the runner, the folder is duplicated to a build location
- The "build" branch is checked-out
- The build python script is launched, a new package is created
- The package is pushed on GitLab
- The CI process triggers the "wex-api" for pulling last version on the wex-apt-repo
- The wex-apt-repo downloads and exposes the package
- The next monday, n8n detects the new version
- n8n triggers "wex-api"
- The wex-api launches Ansible