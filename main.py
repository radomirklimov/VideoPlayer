import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QTimer
import requests
import re

#to get video duration from YouTube API
API_KEY = "AIzaSyA7ER10C8LKtKJCaJQZk_3DQXa8xHct-CI"

class YouTubePlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cartoon Player")
        self.setGeometry(300, 100, 900, 600)

        self.video_urls = [
            "https://www.youtube.com/embed/8DvywoWv6fI?autoplay=1&rel=0",
            "https://www.youtube.com/embed/W6NZfCO5SIk?autoplay=1&rel=0",
            "https://www.youtube.com/embed/Z1Yd7upQsXY?autoplay=1&rel=0",
            "https://www.youtube.com/embed/Q33KBiDriJY?autoplay=1&rel=0",
            "https://www.youtube.com/embed/yRpLlJmRo2w?autoplay=1&rel=0",
            "https://www.youtube.com/embed/7NWN3wivxhA?autoplay=1&rel=0"
        ]

        self.cur_video = 0

        self.layout = QVBoxLayout()
        self.video_view = QWebEngineView()
        self.layout.addWidget(self.video_view)
        self.setLayout(self.layout)

        self.next_button = QPushButton("▶ Next Video")
        self.next_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ff7e5f, stop:1 #feb47b
                );
                color: white;
                font-size: 18px;
                font-weight: bold;
                border-radius: 12px;
                padding: 12px 20px;
            }
            QPushButton:hover {
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:0,
                    stop:0 #feb47b, stop:1 #ff7e5f
                );
            }
            QPushButton:pressed {
                background-color: #e6735c;
            }
        """)
        self.next_button.clicked.connect(self.load_random_video)
        self.layout.addWidget(self.next_button)


        self.load_random_video()

        # Automatically load next video every 60 minutes (you can change this)
        self.timer = QTimer()
        self.timer.timeout.connect(self.load_random_video)
        self.timer.start(self.get_duration(self.cur_video))  # 60 minutes

    def load_random_video(self):
        url = random.choice(self.video_urls)
        while (url == self.cur_video):
            url = random.choice(self.video_urls)
        self.cur_video = url
        self.video_view.load(QUrl(url))

    def get_duration(self, video_url):
        # Extract video ID from URL
        video_id = re.search(r"embed/([a-zA-Z0-9_-]+)", video_url).group(1)

        # Call YouTube API
        api_url = (
            f"https://www.googleapis.com/youtube/v3/videos"
            f"?id={video_id}&part=contentDetails&key={API_KEY}"
        )
        response = requests.get(api_url).json()

        # ISO 8601 duration format (e.g., PT1H2M10S)
        iso_duration = response["items"][0]["contentDetails"]["duration"]
            
        pattern = re.compile(
        r'P(?:T)?'         # Start with P and optional T
        r'(?:(\d+)H)?'     # Hours
        r'(?:(\d+)M)?'     # Minutes
        r'(?:(\d+)S)?'     # Seconds
        )
        match = pattern.match(iso_duration)
        if not match:
            return 0

        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)

        total_ms = ((hours * 3600) + (minutes * 60) + seconds) * 1000
        return total_ms

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = YouTubePlayer()
    player.show()
    sys.exit(app.exec_())
