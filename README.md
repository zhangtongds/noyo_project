# noyo_project

## Summary

## About the Developer

HouseMap was created by Tong Zhang, a software engineer in Mountain View, CA. Learn more about the developer on [LinkedIn](https://www.linkedin.com/in/tong--zhang/).

## Tech Stack

Python, Flask, SQLAlchemy, PostgreSQL

## Setup/Installation

### Requirements

- PostgreSQL
- Python

Please follow the below steps to have this app running on your computer:

Clone repository:

```
$ git clone https://github.com/zhangtongds/noyo_project.git
```

Create a virtual environment:

```
$ virtualenv env
```

Activate the virtual environment:

```
$ source env/bin/activate
```

Install dependencies:

```
$ pip install -r requirements.txt
```

Create database 'person':

```
$ createdb person
```

Create your database tables:

```
$ python
$ from server import db
$ db.create_all()
$ exit()
```

Run the app from the command line in watch mode:

```
$FLASK_APP=server.py FLASK_ENV=development flask run
```

## Results
