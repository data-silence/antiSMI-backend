# antiSMI Backend

![logo](https://github.com/data-silence/antiSMI-backend/blob/master/img/Backend.jpg?raw=true)

![Fastapi](https://img.shields.io/badge/Fastapi-black?style=flat-square&logo=fastapi) ![Pydantic](https://img.shields.io/badge/Pydantic-black?style=flat-square&logo=Pydantic) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-black?style=flat-square&logo=PostgreSQL) 

## Table of contents
* [About](#about)
* [Self deploy](#self-deploy)
* [Stack](#stack)
* [Plans](#plans)
* [Contact info](#contact-info)


## About

The Backend is a fundamental component of the [AntiSMI project](https://github.com/data-silence/antiSMI-Project). It operates asynchronously using the FastAPI framework.
This API retrieves various views of news articles stored in the project databases. The backend gets these views to the frontend of applications developed within the project, including Web-App, AntiSMI-bot and Timemachine-bot.


## Self deploy

Important: you will not be able to deploy the API without access to a specially prepared database.  

1. Clone the repository into the empty directory selected for the project:
`git clone https://github.com/data-silence/antiSMI-backend`
2. Make sure that docker is installed on the server. Build the image from the destination directory using the command `docker build -t -backend`
3. Start the container using `docker run -d --rm --name backend -p 8000:8000 backend`
4. Your API server will start on port 8000


## Stack

* **Framework:** FastAPI
* **Language:** python, sqlalchemy
* **Databases:** postgreSQL, pgvector
* **Validation:** pydantic
* **Server:** gunicorn


## Plans
* make registration and authorisation for limited access to API

## Contact info
* enjoy-ds@pm.me
