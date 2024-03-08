from datetime import datetime
from pymongo import ASCENDING, IndexModel
from pydantic import BaseModel

class WikipediaAnalyzedData(BaseModel):
    title: str
    summary: str
    themes: str
    trends: str
    insights: str
    created_at: datetime = datetime.utcnow()
    
    def to_dict(self):
        return {
            "title": self.title,
            "summary": self.summary,
            "themes": self.themes,
            "trends": self.trends,
            "insights": self.insights,
            "created_at": self.created_at
        }


# Define indexes for faster querying
WikipediaArticleIndexes = [
    IndexModel([('title', ASCENDING)], unique=True),
    IndexModel([('created_at', ASCENDING)])
]
