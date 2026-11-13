from pydantic import BaseModel

class PostsCreate(BaseModel):
    post_poster_name: str
    post_content: str
    post_date: str