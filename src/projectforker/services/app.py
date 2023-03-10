import json

import requests as requests
from fastapi import FastAPI, Form, Depends, Response, status
from fastapi.security import HTTPBearer

from projectforker.models.RepoParameters import RepoParameters

app = FastAPI()
from jose import jwt

SECRET_KEY = "YEKTERCRESYOJHTLAEH"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
oauth2_scheme = HTTPBearer()

FORK_URL = "https://api.github.com/repos"


class MockDB:
    """
        Mock DB Class:
        Holds usernames and passwords that can login and create forks.

        all valid usernames and passwords are stored as a dictionary.

        Username and password

    """
    _username_and_password_dict = {
        "jimmy": "jimmypassword",
        "username": "password",
        "admin": "admin",
        "harry": "potter"
    }

    def authenticate(self, username: str, password: str):
        if username not in self._username_and_password_dict:
            raise Exception("Invalid username cannot authenticate")
        else:
            if password != self._username_and_password_dict[username]:
                raise Exception("Wrong password cannot authenticate")
            else:
                return True

    def verifyJwt(self, jwt):
        return True

    def createUser(self, username, password):
        self._username_and_password_dict[username] = password


def mock_db():
    return MockDB()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/login")
async def login(username: str = Form(), password: str = Form(), db=Depends(mock_db)):
    """
    Login using a username and password. If username and password are correct it returns a jwt. The jwt is used to authenticate into github and create a fork. JWTS are not created by github.
    This jwt is fake and doesn't work.

    In order to login and successfully create a jwt you need to setup an organization a repo and several other parameters.

    This is mock method that does a lot of the similar processes but doesn't fully work.

    https://docs.github.com/en/apps/creating-github-apps/creating-github-apps/creating-a-github-app

    https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token


    """
    db.authenticate(username, password)
    data = {"username": username, "password": password, "fakegithubjwt": True}
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return {"jwt": encoded_jwt}


@app.post("/forkProject")
async def forkProject(repoParameters: RepoParameters, response: Response, db=Depends(mock_db),
                      jwt: str = Depends(oauth2_scheme)):
    """
    This method takes the jwt from the login step and authorizes it in the authentication bearer piece.
    and makes a call to github.

    https://docs.github.com/en/rest/repos/forks?apiVersion=2022-11-28#create-a-fork

    As the jwt token is fake it will fail.

    :param repoParameters:
    :param db:
    :param jwt:
    :return:
    """
    db.verifyJwt(jwt)
    headers = {
        "Authorization": f"Bearer {jwt}",
        "Accept": "application/vnd.github",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    body = {
        "organization": repoParameters.organization,
        "name": repoParameters.fork_name,
        "default_branch_only": True
    }
    fork_response = requests.post(url=f"{FORK_URL}/{repoParameters.owner}/{repoParameters.repo}/forks", headers=headers,
                                  json=body)
    response.status_code = fork_response.status_code
    return fork_response.json()


@app.post("/user", status_code=201)
async def createUser(username: str = Form(), password: str = Form(), db=Depends(mock_db)):
    db.createUser(username, password)
    return {"username": username}
