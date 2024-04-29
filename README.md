# antiSMI Backend

![logo](https://github.com/data-silence/antiSMI-backend/blob/master/img/Backend.jpg?raw=true)

## Table of contents
* [About](#about)
* [Usage](#usage)
* [Stack](#stack)
* [Plans](#plans)
* [Contact info](#contact-info)


## About

The Backend is the foundation for the AntiSMI project, which is async and based on the FastAPI framework.
Serves to retrieve various views of news items stored in the project databases.
Used by the frontend of the applications created within the project: Web-App, AntiSMI-bot and Timemachine-bot.  

## Usage

Important: you will not be able to deploy the API without access to a specially prepared database.  

1. Clone the repository into the empty directory selected for the project:
`git clone https://github.com/data-silence/antiSMI-backend`
2. Make sure that docker is installed on the server. Build the image from the destination directory using the command `docker build -t -backend`
3. Start the container using `docker run -d --rm --name backend -p 8000:8000 backend`
4. Your API server will start on port 8000


## Stack

* **Language:** python, sqlalchemy
* **Databases:** postgreSQL, pgvector
* **Validation:** pydantic
* **Server:** gunicorn


## Plans
* make registration and authorisation for limited access to API

## Contact info
* enjoy-ds@pm.me
