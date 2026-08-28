import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import syncedlyrics

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Lyrics API is live. Go to /docs to test endpoints."}

@app.get("/download")
def get_lyrics(query: str):
    try:
        # 1. Clean filename of invalid characters
        safe_query = "".join(c for c in query if c.isalnum() or c in (" ", "_", "-")).strip()
        txt_filename = f"{safe_query}.txt"

        # 2. Search for synced lyrics across multiple providers
        print(f"Fetching synced lyrics for: {query}...")
        lyrics_text = syncedlyrics.search(query, providers=['Lrclib', 'NetEase', 'Megalobiz'])

        if not lyrics_text:
            raise HTTPException(status_code=404, detail="Synced lyrics not found for this song.")

        # 3. Save to a temporary .txt file
        with open(txt_filename, "w", encoding="utf-8") as f:
            f.write(lyrics_text)

        # 4. Return the .txt file to client
        return FileResponse(
            path=txt_filename,
            filename=txt_filename,
            media_type="text/plain"
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching lyrics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")
