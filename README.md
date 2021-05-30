# noyo_project

## Summary

## About the Developer

This project was created by Tong Zhang, a software engineer in Mountain View, CA. Learn more about the developer on [LinkedIn](https://www.linkedin.com/in/tong--zhang/).

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

Create a user
<img width="1391" alt="Screen Shot 2021-05-29 at 8 14 24 PM" src="https://user-images.githubusercontent.com/28516028/120090835-7982d700-c0ba-11eb-9f1f-0e97df53001b.png">

Get a single user
<img width="1403" alt="Screen Shot 2021-05-29 at 8 15 28 PM" src="https://user-images.githubusercontent.com/28516028/120090849-9e774a00-c0ba-11eb-96e4-58c1d5ab9522.png">

Update user info
<img width="1396" alt="Screen Shot 2021-05-29 at 8 16 45 PM" src="https://user-images.githubusercontent.com/28516028/120090871-cd8dbb80-c0ba-11eb-8ba2-1ec02f4c607a.png">

Get single user with the new version number(default)
<img width="1412" alt="Screen Shot 2021-05-29 at 8 18 15 PM" src="https://user-images.githubusercontent.com/28516028/120090911-02017780-c0bb-11eb-84d5-86e5a37fc118.png">

Get single user with the old version number
<img width="1429" alt="Screen Shot 2021-05-29 at 8 18 50 PM" src="https://user-images.githubusercontent.com/28516028/120090922-18a7ce80-c0bb-11eb-9cff-a03dbda96f6d.png">

Delete user
<img width="1422" alt="Screen Shot 2021-05-29 at 8 19 36 PM" src="https://user-images.githubusercontent.com/28516028/120090935-32491600-c0bb-11eb-8acf-e3c4bfd6b1e1.png">

Get all users
<img width="1395" alt="Screen Shot 2021-05-29 at 8 21 41 PM" src="https://user-images.githubusercontent.com/28516028/120090967-7c31fc00-c0bb-11eb-9d1e-d6afd12a55e9.png">

The database

<img width="735" alt="Screen Shot 2021-05-29 at 8 27 30 PM" src="https://user-images.githubusercontent.com/28516028/120091063-4c372880-c0bc-11eb-8352-8320d476868b.png">

<img width="925" alt="Screen Shot 2021-05-29 at 8 22 16 PM" src="https://user-images.githubusercontent.com/28516028/120090974-91a72600-c0bb-11eb-846f-411b3455cd59.png">





