# Healthjoy Take Home Assignment
### Github forker

### Primary Sources
- https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#handle-jwt-tokens
- https://stackoverflow.com/questions/62994795/how-to-secure-fastapi-api-endpoint-with-jwt-token-based-authorization
- https://docs.github.com/en/rest/repos/forks?apiVersion=2022-11-28#create-a-fork

### How to run?
1. python3 -m venv venv
2. pip install -r requirements.txt
3. Run uvicorn on the app file.
```
uvicorn projectforker.services.app:app
```
4. fastapi docs should be available at.
```
http://localhost:8000/docs
```

### Rest calls
1. Login user the username a password. (Creates a fake jwt token)
2. Take the jwt token and go to the authorize section to the side and copy the jwt into the field
3. Go to the /forkProject end point and specificy parameters.
