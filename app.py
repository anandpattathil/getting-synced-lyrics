import flet as ft
import requests
import os

# Replace with your actual live Render URL
API_URL = "https://syncyolyrics.onrender.com/download"

def main(page: ft.Page):
    page.title = "Lyrics Downloader"
    page.padding = 20

    status_text = ft.Text("", size=14)

    # Clears status text as soon as the user starts typing a new song
    def on_text_change(e):
        status_text.value = ""
        page.update()

    song_input = ft.TextField(
        label="Enter Song Name (e.g., Timeless Weeknd)",
        width=350,
        on_change=on_text_change
    )

    def download_lyrics(e):
        if not song_input.value.strip():
            status_text.value = "Please enter a song name."
            status_text.color = "red"
            page.update()
            return

        query = song_input.value.strip()
        
        # Immediate UI feedback to signal the search started
        status_text.value = f"Searching lyrics for '{query}'..."
        status_text.color = "blue"
        page.update()

        try:
            response = requests.get(API_URL, params={"query": query}, timeout=30)
            
            if response.status_code == 200:
                safe_name = "".join(c for c in query if c.isalnum() or c in (" ", "_", "-")).strip()
                
                android_path = "/sdcard/Download"
                if os.path.exists(android_path):
                    file_path = f"{android_path}/{safe_name}.txt"
                else:
                    file_path = f"{safe_name}.txt"

                with open(file_path, "wb") as f:
                    f.write(response.content)

                status_text.value = f"Saved: {safe_name}.txt!"
                status_text.color = "green"
            elif response.status_code == 404:
                status_text.value = "Lyrics not found. Try adding the main artist name (e.g., The Weeknd Timeless)."
                status_text.color = "orange"
            else:
                status_text.value = f"Error: Server returned status code {response.status_code}"
                status_text.color = "red"

        except Exception as err:
            status_text.value = f"Connection Error: {err}"
            status_text.color = "red"

        page.update()

    page.add(
        ft.Text("Synced Lyrics Downloader (.txt)", size=20, weight="bold"),
        song_input,
        ft.ElevatedButton("Download Lyrics", on_click=download_lyrics),
        status_text
    )

ft.app(target=main)
