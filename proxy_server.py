# ==========================================================
# 🌍 Proxy Server for Book & Movie Recommender
# By Parsa — Handles TMDB + Google Books API Requests
# ==========================================================

from fastapi import FastAPI, Query
import httpx
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")


@app.get("/")
def home():
    """Health check"""
    return {"message": "✅ Proxy Server is running successfully!"}


# ==========================================================
# 🎬 TMDB ENDPOINTS
# ==========================================================

@app.get("/tmdb/genres")
async def get_tmdb_genres():
    """Get TMDB movie genres"""
    async with httpx.AsyncClient() as client:
        url = "https://api.themoviedb.org/3/genre/movie/list"
        params = {"api_key": TMDB_API_KEY, "language": "en-US"}
        res = await client.get(url, params=params, timeout=15)
        res.raise_for_status()
        return res.json()


@app.get("/tmdb/discover")
async def discover_movies(
    with_genres: int = Query(..., alias="with_genres"),
    primary_release_year: int = Query(..., alias="primary_release_year"),
    page: int = 1
):
    """Get movies by genre and year"""
    async with httpx.AsyncClient() as client:
        url = "https://api.themoviedb.org/3/discover/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "with_genres": with_genres,
            "primary_release_year": primary_release_year,
            "language": "en-US",
            "sort_by": "popularity.desc",
            "page": page,
            "include_adult": False,
        }
        res = await client.get(url, params=params, timeout=15)
        res.raise_for_status()
        return res.json()


# ==========================================================
# 📚 GOOGLE BOOKS ENDPOINT
# ==========================================================

@app.get("/books/search")
async def search_books(
    q: str,
    maxResults: int = 40,
    orderBy: str = "relevance",
    printType: str = "books",
):
    """Search books from Google Books API"""
    async with httpx.AsyncClient() as client:
        url = "https://www.googleapis.com/books/v1/volumes"
        params = {
            "q": q,
            "maxResults": maxResults,
            "orderBy": orderBy,
            "printType": printType,
            "key": GOOGLE_BOOKS_API_KEY,
        }
        res = await client.get(url, params=params, timeout=15)
        res.raise_for_status()
        return res.json()
