import flet as ft
import requests

# Set this to your actual deployed Render URL
BACKEND_URL = "https://syncyolyrics.onrender.com/download"

def main(page: ft.Page):
    page.title = "syncYolyrics"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = ft.Padding.all(20)
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    title_text = ft.Text("syncYolyrics", size=30, weight=ft.FontWeight.BOLD)

    song_input = ft.TextField(
        label="Song Title / Artist",
        hint_text="e.g. Euphoria Kendrick Lamar",
        width=350,
        autofocus=True
    )

    status_text = ft.Text("", size=14)

    lyrics_display = ft.TextField(
        label="Fetched Synced Lyrics (.lrc)",
        multiline=True,
        min_lines=8,
        max_lines=12,
        width=350,
        read_only=True,
        visible=False
    )

    def download_click(e):
        query = song_input.value.strip() if song_input.value else ""
        if not query:
            status_text.value = "Please enter a song name or artist."
            status_text.color = ft.Colors.RED_400
            page.update()
            return

        status_text.value = "Searching for synced lyrics..."
        status_text.color = ft.Colors.BLUE_300
        lyrics_display.visible = False
        page.update()

        try:
            response = requests.get(
                f"{BACKEND_URL}/search",
                params={"query": query},
                timeout=20
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    status_text.value = "Lyrics downloaded successfully!"
                    status_text.color = ft.Colors.GREEN_400
                    lyrics_display.value = data.get("lyrics", "")
                    lyrics_display.visible = True
                else:
                    status_text.value = data.get("message", "Lyrics not found.")
                    status_text.color = ft.Colors.RED_400
            else:
                status_text.value = f"Server Error ({response.status_code})"
                status_text.color = ft.Colors.RED_400

        except Exception as err:
            status_text.value = "Failed to connect to backend server."
            status_text.color = ft.Colors.RED_400

        page.update()

    download_btn = ft.ElevatedButton(
        "Download .lrc",
        icon=ft.Icons.DOWNLOAD,
        on_click=download_click
    )

    page.add(
        title_text,
        ft.Container(height=10),
        song_input,
        ft.Container(height=10),
        download_btn,
        ft.Container(height=15),
        status_text,
        ft.Container(height=10),
        lyrics_display
    )

ft.app(target=main)
