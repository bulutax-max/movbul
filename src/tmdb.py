import os
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE = "https://api.themoviedb.org/3"
IMG_BASE = "https://image.tmdb.org/t/p"

def _get(path, params=None):
    if not TMDB_API_KEY:
        raise RuntimeError("TMDB_API_KEY bulunamadı. .env dosyanızı kontrol edin.")
    params = params or {}
    params["api_key"] = TMDB_API_KEY
    url = f"{BASE}{path}?{urlencode(params)}"
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return r.json()

def get_genres():
    data = _get("/genre/movie/list", {"language": "tr-TR"})
    return data.get("genres", [])

def discover_movies(genre_ids=None, sort_by="vote_average.desc", page=1, min_votes=200):
    params = {
        "include_adult": "false",
        "include_video": "false",
        "language": "tr-TR",
        "sort_by": sort_by,
        "page": page,
        "vote_count.gte": min_votes
    }
    if genre_ids:
        params["with_genres"] = ",".join(map(str, genre_ids))
    return _get("/discover/movie", params)

def search_movies(query, page=1):
    if not query:
        return {"results": []}
    params = {"query": query, "language": "tr-TR", "page": page, "include_adult": "false"}
    return _get("/search/movie", params)

def trending(period="week", page=1):
    # period: "day" | "week"
    params = {"language": "tr-TR", "page": page}
    return _get(f"/trending/movie/{period}", params)

def poster_url(path, size="w342"):
    if not path:
        return None
    return f"{IMG_BASE}/{size}{path}"
