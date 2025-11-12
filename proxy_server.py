from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# اجازه دسترسی از Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # برای تست عمومی، بعداً میشه محدود کرد
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")

@app.get("/tmdb")
def tmdb_proxy(endpoint: str, params: str = ""):
    """Proxy برای TMDB"""
    url = f"https://api.themoviedb.org/3/{endpoint}?api_key={TMDB_API_KEY}&{params}"
    resp = requests.get(url)
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()

@app.get("/books")
def books_proxy(q: str, maxResults: int = 10):
    """Proxy برای Google Books"""
    url = (
        f"https://www.googleapis.com/books/v1/volumes?q={q}"
        f"&maxResults={maxResults}&key={GOOGLE_BOOKS_API_KEY}"
    )
    resp = requests.get(url)
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()
