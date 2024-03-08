from fastapi import APIRouter, HTTPException
from database.connection import MongoDBConnection
from database.data_models import WikipediaAnalyzedData

router = APIRouter()

# Initialize MongoDB connection
mongo_conn = MongoDBConnection(
    host="mongodb",
    port=27017,
    username="username",
    password="password",
    database_name="wikipedia_db",
)
if mongo_conn.connect():
    db = mongo_conn.db
else:
    raise HTTPException(status_code=500, detail="Failed to connect to the database.")


@router.get("/articles/{article_id}")
async def get_article(article_id: str):
    """
    Retrieve an analyzed Wikipedia article by its ID.
    """
    article = db.articles.find_one({"_id": article_id})
    if article:
        return article
    else:
        return None


@router.post("/articles")
async def create_article(article: WikipediaAnalyzedData):
    """
    Create a new analyzed Wikipedia article.
    """
    result = db.articles.insert_one(article.to_dict())
    return {"id": str(result.inserted_id)}


@router.put("/articles/{article_id}")
async def update_article(article_id: str, article: WikipediaAnalyzedData):
    """
    Update an existing analyzed Wikipedia article.
    """
    result = db.articles.replace_one({"_id": article_id}, article.to_dict())
    if result.modified_count == 1:
        return {"message": "Article updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Article not found")


@router.delete("/articles/{article_id}")
async def delete_article(article_id: str):
    """
    Delete an analyzed Wikipedia article by its ID.
    """
    result = db.articles.delete_one({"_id": article_id})
    if result.deleted_count == 1:
        return {"message": "Article deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Article not found")
