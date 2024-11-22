from fastapi import FastAPI
import imageMatcher
import asyncio

# Initialize FastAPI app
app = FastAPI()

# API endpoint
@app.get("/timeline_info/")
async def get_JSON():
    file_path = "/app/en.wikipedia.org_detail.json"
    artist_name = "The Beatles"
    final_json = await imageMatcher.fact_imager(file_path, artist_name)
    return (final_json)
