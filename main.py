from fastapi import FastAPI
import syncedlyrics

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "syncYolyrics API is online"}

@app.get("/search")
def search_lyrics(query: str):
    if not query:
        return {"success": False, "message": "Search query cannot be empty."}
    
    try:
        lrc = syncedlyrics.search(query)
        if lrc:
            return {"success": True, "lyrics": lrc}
        return {"success": False, "message": "No synced lyrics found for this track."}
    except Exception as e:
        return {"success": False, "message": f"Search error: {str(e)}"}
