# oauth-service
This is a simple OAuth2 service that can be used to authenticate users against a mongoDB database.

## Installation
The project uses poetry for dependency management.
THe easiest way to install poetry is to run the following command:

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

To install the dependencies, run the following command:

```bash
poetry install
```

OR
To install just the base dependencies, run the following command:

```bash
pip install -r requirements.txt
```

## Running the service
The service can be run using Docker.

```bash
docker-compose build
```

```bash
docker-compose up
```

## Running the tests
The tests can be run using the following command:

```bash
pytest .
```

## API Documentation
The service exposes the following endpoints:

### /user/register
This endpoint is used to register a new user.
```
:param username: username of the user
:param password: password of the user
:param admin: admin status of the user
:return: user registered message"
```

### /user/login
This endpoint is used to login a user.
```
:param username: username of the user
:param password: password of the user
:return: JWT access token
```

### /register/client
This endpoint is used to register a new client.
```
:param client_id: client id of the client
:param name: name of the client
:param username: username of the client
:param password: password of the client
:return: client_Id  and client_secret
```

### /kyc/apply
This endpoint is used to apply for KYC and uses JWT token for authentication.
```
:param username: username of the user
:param password: password of the user
:param kyc_id: kyc id of the user
:param kyc_type: kyc type of the user
:param kyc_data: kyc data of the user
```
### /kyc/approve
This endpoint is used to approve KYC and requires oauth2 for authentication.
```
:param username: username of the user
```

### Oauth flow
The oauth flow is as follows:
#### /oauth/authorize
This endpoint is used to authorize the client.
```
:param client_id: client id of the client
:param response_type: response type of the client
:param scope: scope of the client
:param state: state of the client
:param redirect_uri: redirect uri of the client with the code
```

````bash
    curl --location 'http://0.0.0.0:8000/oauth/authorize?scope=kyc_status&client_id=aa1&response_type=code' \
    --header 'Content-Type: application/json' \
    --data '{"username":"u1",
    "password":"p",
    "client_id":"aa",
    "scope":"kyc_status"
    }'
```

#### /oauth/token
This endpoint is used to get the access token.
```
:param client_id: client id of the client
:param client_secret: client secret of the client
:param grant_type: grant type of the client
:param code: code of the client
:param redirect_uri: redirect uri of the client with the code
:return: access token
```

````bash
curl --location --request POST 'localhost:8000/oauth/token?client_id=aa1&grant_type=authorization_code&code=5VoOlZbmeK3aOXMkNnpwi9G9TIpdHZ&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Foauth%2Fauthorized' \
--data ''
```

#### /oauth/revoke
This endpoint is used to revoke the access token.
```
:param token: access token of the client
:return: revoked message
```

## Testing the service
The service can be tested using the following command:

```bash
pytest .
```

## TODOS/ Things to improve
- Add more tests
- Add more documentation
- Add swagger documentation
- Oauth approval page(Currently works though user login)
- Split the database into multiple databases(For oauth and kyc)
- Docker network for the service(Currently using host mode)
- Limit available scopes
