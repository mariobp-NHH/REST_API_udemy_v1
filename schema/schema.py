from pydantic import BaseModel

class ArticleSchema(BaseModel):
    title:str 
    description:str 

class ArticleSchemaOut(ArticleSchema):
    title:str 
    description:str 

    class Config:
        orm_mode = True