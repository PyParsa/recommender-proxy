# ==========================================================
# 🌐 Recommender Proxy Server
# Designed by Parsa | Powered by FastAPI
# ==========================================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI(title="Book & Movie Recommender Proxy")

# CORS setup - اجازه اتصال از Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # بعداً اگه خواستی، فقط دامنه Streamlit رو بذار
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# محیط متغیرها
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")

@app.get("/")
def home():
    return {"message": "✅ Proxy Server is running successfully!"}

@app.get("/tmdb")
async def tmdb_proxy(endpoint: str, params: dict = {}):
    """پروکسی برای TMDB"""
    try:
        url = f"https://api.themoviedb.org/3/{endpoint}"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params={**params, "api_key": TMDB_API_KEY})
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/books")
async def books_proxy(q: str):
    """پروکسی برای Google Books"""
    try:
        url = f"https://www.googleapis.com/books/v1/volumes"
        params = {"q": q, "key": GOOGLE_BOOKS_API_KEY, "maxResults": 40, "printType": "books"}
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params)
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
