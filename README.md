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

### Run project

**The following steps show how to run project locally(i.e., with DEBUG=True)**

Generate `SECRET KEY` for your project, using the following code:
```python
    import secrets

    secret_key = secrets.token_hex(34)

    print(secret_key)
```

In root directory create file `.env`(**check that this file is in `.gitignore`**) and add the following line:
```
    SECRET_KEY=<your_secret_key>
```

Then you need to create `PostgreSQL` database(using pgAdmin or any other tool), using `SQL` statement:
```SQL
    CREATE DATABASE <your_database_name>;
```

Next, go to `.env` and, using your database credentials, add the following lines:
```
    DB_NAME=<your_database_name>
    DB_USER=<your_database_user>
    DB_PASSWORD=<your_database_password>
    DB_HOST=<your_database_host>
    DB_PORT=<your_database_port>
```

After that, in command line run:
```
    python manage.py migrate
    python manage.py runserver
```

Go to your browser at the address: 'http://127.0.0.1:8000/', you will see:
```JSON
    {
        "is_root": true
    }
```
Visit url: 'http://127.0.0.1:8000/docs', you will see interactive documentation provided by `OpenAPI`.


### Usage specifics

This API uses `Oauth2` specification to define to handle authentication and authorization. To authenticate users need to provide header `Authorization` with value 'Bearer ' + `JWT`(JSON Web Token) token. You can get this token using path: '/auth/token', entering your username and password(if registered before this), if your credentials are valid, you will get response like this:
```JSON
    {
        "access_token": "<generated_token>",
        "token_type": "bearer"
    }
```

Use this generated token in headers in your subsequent requests.

**Make sure that you send username and password as `form-data`, as this is required by `Oauth2`.**

If you are not using using any clients to interact with API, interactive docs allow you to authenticate using `Authorize` button in the top right corner.


### API Endpoints

`default`
* `GET` '/' - API's root

`users`
* `POST` '/auth/register' - register
* `POST` '/auth/token' - login for access token
* `GET` '/users/me' - get currently authenticated user's credentials
* `PATCH` '/users/me' - update currently authenticated user's credentials

`recommendations`
* `GET` '/recommendations' - get recommendation-list (query parameters can be provided)
* `POST` '/recommendations' - post new recommendation(accessible only by authenticated users)
* `GET` '/recommendations/{recommendation_id}' - get recommendation-detail
* `PATCH` '/recommendations/{recommendation_id}' - update recommendation(accessible only be author of the recommendation)
* `DELETE` '/recommendations/{recommendation_id}' - delete recommendation(accessible only be author of the recommendation)

`comments`
* `GET` '/recommendations/{recommendation_id}/comments' - get comment-list (query parameters can be provided)
* `POST` '/recommendations{recommendation_id}/comments' - post new comment(accessible only by authenticated users)
* `GET` '/recommendations/{recommendation_id}/comments/{comment_id}' - get comment-detail
* `PATCH` '/recommendations/{recommendation_id}/comments/{comment_id}' - update comment(accessible only be author of the comment)
* `DELETE` '/recommendations/{recommendation_id}/comments/{comment_id}' - delete comment(accessible only be author of the comment)

`reactions`
* `GET` '/recommendations/{recommendation_id}/reactions' - get reaction-list (query parameters can be provided)
* `POST` '/recommendations{recommendation_id}/reactions' - post new reaction(accessible only by authenticated users)
* `GET` '/recommendations/{recommendation_id}/reactions/{reaction_id}' - get reaction-detail
* `PATCH` '/recommendations/{recommendation_id}/reactions/{reaction_id}' - update reaction(accessible only be author of the reaction)
* `DELETE` '/recommendations/{recommendation_id}/reactions/{reaction_id}' - delete reaction(accessible only be author of the reaction)

### Testing

This API uses `Python`'s module `pytest` for running tests. All test modules as well as 'conftest.py' are
in directory 'tests'. In 'conftest.py' you can find some `fixtures` used by tests.

To run all tests, in command line run:
```
    pytest
```

To run particular module, run:
```
    pytest tests/test_users.py
```

To run particular test in a module, run:
```
    pytest tests/test_auth.py::test_register 
``` 