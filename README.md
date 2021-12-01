# MMIB-ApiGateway-Submodule
Api Gateway implementation for the microservices-based application MMIB. 
This is the source code of Message in a Bottle application, self project of *Advanced Software Engineering* course,
University of Pisa.



## Team info

- The *squad id* is **10**
- The *team leader* is Giuseppe Crea

#### Members

| Name and Surname  | Email |
| ----------------  | ----- |
|Giuseppe Crea      |       |
|Francesco Venturini|f.venturini12@studenti.unipi.it|
|Ivan Sarno         |       |
|Francesco Gargiulo |       |
|                   |       |


## Instructions

### Initialisation

To setup the project initially you have to run these commands
inside the project's root.

`virtualenv -p python3 venv`

`source venv/bin/activate`

`pip install -r requirements.dev.txt`

### Run the project

To run the project you have to setup the flask environment,
you can do it by executing the following command:

`export FLASK_ENV=<environment-name>`

and now you can run the application

`flask run`
