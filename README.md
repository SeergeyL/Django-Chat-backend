# Django-Chat-backend
Chat with friend system. Users can send friend requests and accept them or reject. You can communicate only with users 
that are in your friend list.

## Stack

- Django
- Django REST Framework
- Django Channels
- Docker
- Redis
- PostgreSQL

## Setup

To start the project you should clone the repository and create `.env` file in the project directory. 
For test run you can use environment variables below.
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
```

Start the project using docker. It will create and run migrations and start the server on `127.0.0.1:8000`
```
docker-compose up --build
```

You can create superuser:
```
docker exec -ti <CONTAINER_ID> python manage.py createsuperuser
```

And run tests:
```
docker exec -ti <CONTAINER_ID> pytest
```

## API
API documentation is available at `127.0.0.1:8000/redoc`

User registration algorithm:
- Send request with *username*, *email*, *password*, *password2* fields to `/api/v1/register/`
- Then you can get your authentication token by sending *username* and *password* to `/api/v1/api-token-auth/`


## WebSocket connection
You can connect to backend websocket on your frontend by the following way. Connection will be accepted if `username`
in your friend list, and you provided the authentication `token`
```javascript
let ws = new WebSocket('ws://127.0.0.1:8000/ws/chat/{username}/?token={token}')
```

Examle of sending data to backend WebSocket
```javascript
let msg = {
    'command': 'MESSAGE:SEND',
    'message': 'Hello world!'
}
ws.send(JSON.stringify(msg))
```


