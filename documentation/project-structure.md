# Project Structure

This repository contains two distinct sub-projects:
* data-updater – handles metadata auditing and scoring
* rest-api – serves the audit results via a web API

> While each component could ideally reside in its own repository, they are maintained together here for organizational purposes.

Each sub-project includes:
* A clear entry point (`main.py` or `app.py`)
* A versioned `requirements.txt` file
* One or more `Dockerfiles` for building and running the project

Additionally, the data-updater sub-project includes a `crontab.txt` file, which defines the execution schedule for automated runs.

```
opendata_audit
│   README.md
│   LICENSE
├───documentation 
├───data-updater
│   │   main.py
│   │   main_debug.py
│   │   Dockerfile.debug
│   │   Dockerfile.prod
│   │   Dockerfile.run-now
│   │   crontab.txt
│   │   requirements.txt
│   ├───data
│   └───data-updater
└───rest-api
    │   app.py
    │   Dockerfile
    │   requirements.txt
    ├───data
    └───templates
```

See [Inter-Process Communication](../documentation/inter-process-communication.md) for an explanation of how the data-updater and rest-api exchange data.
