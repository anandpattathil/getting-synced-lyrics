import os
import re
import requests
import flet as ft

# Set this to your exact Render API endpoint (e.g., /lyrics or /download)
BACKEND_URL = "https://syncyolyrics.onrender.com/download"


def save_lrc_file(song_name: str, lyrics_content: str) -> str:
    # Clean invalid filename characters (e.g., / \ : * ? " < > |)
    safe_name = re.sub(r'[\\/*?:"<>|]', "", song_name).strip()
    if not safe_name:
        safe_name = "synced_lyrics"

    # Target the 'lrc_files' folder in main Internal Storage
    target_dir = "/storage/emulated/0/lrc_files"

    # Fallback for PC testing if Android storage path isn't present
    if not os.path.exists("/storage/emulated/0"):
        target_dir = os.path.join(os.getcwd(), "lrc_files")

    # Automatically create the 'lrc_files' directory if it does not exist
    os.makedirs(target_dir, exist_ok=True)

    file_path = os.path.join(target_dir, f"{safe_name}.lrc")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(lyrics_content)

    return file_path


def main(page: ft.Page):
    page.title = "syncYoLyrics"
    page.theme_mode = ft.ThemeMode.DARK

    # Increase 'top' value to push everything lower on the screen
    page.padding = ft.padding.only(top=80, left=20, right=20, bottom=20)

    song_input = ft.TextField(
        label="Song Title / Artist",
        hint_text="e.g., Blinding Lights - The Weeknd",
        expand=True,
    )
    status_text = ft.Text(size=14)

    def download_click(e):
        query = song_input.value.strip()
        if not query:
            status_text.value = "Please enter a song name."
            status_text.color = ft.Colors.RED_400
            page.update()
            return

        status_text.value = "Searching and downloading synced lyrics..."
        status_text.color = ft.Colors.BLUE_400
        page.update()

        try:
            response = requests.get(
                BACKEND_URL, params={"query": query}, timeout=15
            )

            if response.status_code == 200:
                data = response.json()
                lyrics = data.get("lyrics")

                if lyrics:
                    saved_path = save_lrc_file(query, lyrics)
                    status_text.value = (
                        f"Saved successfully!\nLocation: {saved_path}"
                    )
                    status_text.color = ft.Colors.GREEN_400
                else:
                    status_text.value = "No synced lyrics found for this song."
                    status_text.color = ft.Colors.ORANGE_400
            else:
                status_text.value = (
                    f"Server returned error code: {response.status_code}"
                )
                status_text.color = ft.Colors.RED_400

        except Exception as ex:
            status_text.value = f"Error: {str(ex)}"
            status_text.color = ft.Colors.RED_400

        page.update()

    page.add(
        ft.Column(
            [
                ft.Text("syncYolyrics", size=26, weight=ft.FontWeight.BOLD),
                ft.Row([song_input]),
                ft.ElevatedButton(
                    "Download .lrc",
                    icon=ft.Icons.DOWNLOAD,
                    on_click=download_click,
                ),
                ft.Divider(),
                status_text,
            ],
            spacing=15,
        )
    )

ft.app(target=main)
