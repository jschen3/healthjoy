from pydantic import BaseModel

class RepoParameters(BaseModel):
    owner: str
    repo: str
    organization: str
    fork_name: str