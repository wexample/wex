## Managing Service Dependencies

Each addon can declare its dependencies on other addons, making it easier to manage complex projects. An addon can declare its dependencies through the service.config.json file.

For example, suppose the Matomo addon requires the MySQL addon. In that case, the Matomo addon should create a service.config.json file in the services/matomo folder, with the following content:

    {
      "dependencies": [
        "mysql-8"
      ]
    }
