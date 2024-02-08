from fastapi import FastAPI, Depends, status, HTTPException
import uvicorn
from database.database import engine, SessionLocal
from schema.schema import ArticleSchema, ArticleSchemaOut
from sqlalchemy.orm import Session
import models
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()


@app.get('/articles', response_model=List[ArticleSchemaOut])
def get_articles(db:Session = Depends(get_db)):
    my_articles = db.query(models.Article).all()
    return my_articles 

@app.get('/articles/{id}', status_code=status.HTTP_200_OK, response_model=ArticleSchemaOut)
def article_details(id:int, db:Session = Depends(get_db)):
    my_article = db.query(models.Article).filter(models.Article.id == id).first()

    if my_article:
        return my_article
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The article does not exist")

@app.post('/articles/', status_code=status.HTTP_201_CREATED)
def add_article(article:ArticleSchema, db: Session = Depends(get_db)):
    new_article = models.Article(title = article.title, description=article.description)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

@app.put('/articles/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_article(id:int, article:ArticleSchema, db:Session = Depends(get_db)):
    db.query(models.Article).filter(models.Article.id == id).update({'title':article.title, 'description':article.description})
    db.commit()
    return {"message":"Data is updated"}

@app.delete('/articles/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_data(id:int, db:Session = Depends(get_db)):
    db.query(models.Article).filter(models.Article.id == id).delete(synchronize_session=False)
    db.commit()

if __name__ == "__main__":
    uvicorn.run("application:app", port=8000, log_level="info", reload=True)