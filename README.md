# chatbot-task-bot

## Table of contents
* [General Informations](#general-informations)
* [Installation](#installation)
* [How To Run It?](#how-to-run-it)


## General Informations:

The microsoft teams bot application for project.

## Installation

Make sure that you have installed Poetry with Python 3.12.

Activate the virtual environment of Poetry:
```bash
poetry shell
```

To install dependencies of the project:
```bash
poetry install
```

## How To Run It?

Run

```bash
python src/app.py
```

### Environment Variables

Before running application, you need to export environment variables.

Also, you need to be sure that you have a running backend application.

The variables that you need to export are listed:

```
TEAMS__APP_ID=teams-app-id
TEAMS__APP_PASSWORD=teams-app-secret
BACKEND_API_URL=http://localhost:8000
```



