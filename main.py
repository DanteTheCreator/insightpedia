import asyncio
from collections import deque
import multiprocessing
from fastapi import BackgroundTasks, FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database.data_models import WikipediaAnalyzedData
from api.endpoints import create_article, get_article
from wikipedia import suggest, page
from analysis.analyzer import ContentAnalyzer
import uvicorn

# Initialize FastAPI app
app = FastAPI()

# Queue for pending requests
request_queue = deque()


async def analyze_topic(topic):
    try:
        article = await get_article(topic)
        if article:
            print("Topic already exists in the database!")
        else:
            article = page(topic) or page(suggest(topic))

            analyzer = ContentAnalyzer()
            summary = analyzer.summary(article.content)
            themes = analyzer.key_themes(article.content)
            trends = analyzer.trends(article.content)
            insights = analyzer.insights(article.content)

            new_entry_article = WikipediaAnalyzedData(
                title=article.title,
                summary=summary,
                themes=themes,
                trends=trends,
                insights=insights,
            )
            await create_article(new_entry_article)

    except HTTPException as e:
        print(f"Error: {e.detail}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


async def process_queue():
    while True:
        if request_queue:
            topic = request_queue.popleft()
            await analyze_topic(topic)
        else:
            await asyncio.sleep(1)


# Templates directory
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/")
async def submit_topic(
    request: Request,
    topic: str = Form(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    request_queue.append(topic)
    background_tasks.add_task(process_queue)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "status": 200, "message": f"Received topic: {topic}"},
    )


if __name__ == "__main__":
    import uvicorn
    import warnings

    warnings.filterwarnings("ignore", category=RuntimeWarning)

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
