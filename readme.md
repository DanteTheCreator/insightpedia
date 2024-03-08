# InsightPedia

This project aims to analyze wikipedia articles and save summaries, key themes, trends and insight in a database.

## Table of Contents

- [Installation](#installation)
- [Running](#running)
- [Usage](#usage)

## Pre-requisites:
- Docker
- LM Studio (can use openai)

## Installation
Clone the repository and navigate to the root of the project.
To install and run the project, simply use `docker-compose`:

```bash
docker-compose up --build
```

This command will build the necessary Docker images and start the containers.


## Running
- Build and start containers
- Have a server running in LM Studio, with LLM (app tested on Mistral). *If not using LM Studio, change api link in* ./analysis/analyzer.py

## Usage
- You should be able to visit your localhost:8000 where you should see a single input and submit. You can submit different topics over and over again, app will take care of it in the background. App just submits answrs to the DB per assignment, it does not show results.
