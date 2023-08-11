# FastAPI API for publishing fiction recommendations

### Introduction

This API allows users to share their taste in music, books, movies and any other fiction. This API can be useful for people who are trying to find something to enjoy(new song or book in their favorite genre,for example) as well as to those who are interested in sharing their opinions on different pieces of fiction. Comments and reactions(positive or negative) can be left for each recommendation. 

### Features

* Users can register, login, view their profiles and change their profiles(change username and email).
* Authenticated users can publish, update and delete recommendations.
* Authenticated users can publish, update and delete comments left for recommendations.
* Authenticated users can publish, update and delete reactions left for recommendations. Each user can have only one reaction(either positive or negative) for each recommendation.
* All recommendations, comments and reactions are visible to all users(authenticated as well as non-authenticated).

### Technologies

* `FastAPI`
* `PostgreSQL`

### Project Structure

This API uses `FastAPI`'s routers. For running migrations was used `Alembic`. As ORM tool was used `SQLModel`.

There are four routers in this project:
* `users`
* `recommendations`
* `comments`
* `reactions`

`users` router manages users' registration, login and profile changing. Also each user can see their own profile.
`recommendations` router manages reading, publishing, updating and deleting of recommendations.
`comments` router manages reading, publishing, updating and deleting of comments.
`reactions` router manages reading, publishing, updating and deleting of reactions.

API also has `root` path operation that serves no particular purpose, except that when you start your application and visit path: "/", instead of seeing:
```JSON
    {
        "detail": "Not Found"
    }
```
you will see:
```JSON
    {
        "is_root": true
    }
```

### Installation

**To work with this project you need `Python3.9+` installed on your machine**

If you do not have `Python` installed, 
visit official documentation and install it: https://www.python.org/downloads/

Clone repository, using command:
```
    git clone https://github.com/Andrew-157/fastapi_project_2
```

Then, use command:
```
    cd fastapi_project_2
```

**Everything shown below assumes you are working from directory `fastapi_project_2`**

Required packages:
```
    fastapi==0.100.1
    sqlmodel==0.0.8
    uvicorn==0.23.2
    python-decouple==3.8
    psycopg2-binary==2.9.7
    alembic==1.11.2
    python-jose==3.3.0
    passlib==1.7.4
    python-multipart==0.0.6
    httpx==0.24.1
    pytest==7.4.0
    autopep8==2.0.2
```

If you are using `pipenv` for managing virtual environments, in command line run:
```
    pipenv install
```
And then to activate environment run:
```
    pipenv shell
```

You can also use file `requirements.txt` with pip.
Inside your activated virtual environment, run:
```
    pip install -r requirements.txt
```
For `Windows`
```
    pip3 install -r requirements.txt
```
For `Unix`-based systems