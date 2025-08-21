import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QPushButton
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl 

# Sample playlists
playlists = {
    "Playlist 1": [
        "https://www.youtube.com/embed/dQw4w9WgXcQ",
        "https://www.youtube.com/embed/3JZ_D3ELwOQ"
    ],
    "Playlist 2": [
        "https://www.youtube.com/embed/L_jWHffIx5E",
        "https://www.youtube.com/embed/eY52Zsg-KVI"
    ]
}

class YouTubePlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini YouTube Player")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Playlist list
        self.playlist_list = QListWidget()
        self.playlist_list.addItems(playlists.keys())
        self.layout.addWidget(self.playlist_list)

        # Button to open playlist
        self.open_button = QPushButton("Open Playlist")
        self.layout.addWidget(self.open_button)
        self.open_button.clicked.connect(self.open_playlist)

        # Web view for videos
        self.video_view = QWebEngineView()
        self.layout.addWidget(self.video_view)

        # Current video index
        self.current_index = 0
        self.current_playlist = []

    def open_playlist(self):
        selected_playlist = self.playlist_list.currentItem()
        if selected_playlist:
            self.current_playlist = playlists[selected_playlist.text()]
            self.current_index = 0
            self.play_video(self.current_index)

    def play_video(self, index):
        if 0 <= index < len(self.current_playlist):
            self.video_view.setUrl(QUrl(self.current_playlist[index]))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = YouTubePlayer()
    player.show()
    sys.exit(app.exec())
