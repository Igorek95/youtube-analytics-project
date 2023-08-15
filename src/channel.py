import os
import json

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.title = None
        self.description = None
        self.custom_url = None
        self.published_at = None
        self.thumbnail_url = None
        self.view_count = None
        self.subscriber_count = None
        self.video_count = None

        self.update_info()  # Вызываем метод для обновления информации о канале

    def __str__(self):
        return f'{self.title} -> {self.url}'

    def __add__(self, other):
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        return self.subscriber_count - other.subscriber_count

    def __lt__(self, other):
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        return self.subscriber_count <= other.subscriber_count

    def __eq__(self, other):
        return self.subscriber_count == other.subscriber_count

    def __ne__(self, other):
        return self.subscriber_count != other.subscriber_count

    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        return self.subscriber_count >= other.subscriber_count

    @property
    def channel_id(self):
        """Возвращает ID канала."""
        return self.__channel_id


    def update_info(self):
        """Обновляет информацию о канале из YouTube API."""
        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        if 'items' in channel and len(channel['items']) > 0:
            snippet = channel['items'][0]['snippet']
            statistics = channel['items'][0]['statistics']

            self.title = snippet.get('title', None)
            self.description = snippet.get('description', None)
            self.custom_url = snippet.get('customUrl', None)
            self.published_at = snippet.get('publishedAt', None)
            self.thumbnail_url = snippet['thumbnails']['medium']['url']
            self.view_count = statistics.get('viewCount', None)
            self.subscriber_count = int(statistics.get('subscriberCount', None))
            self.video_count = statistics.get('videoCount', None)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(f"Title: {self.title}")
        print(f"Description: {self.description}")
        print(f"Custom URL: {self.custom_url}")
        print(f"Published At: {self.published_at}")
        print(f"Thumbnail URL: {self.thumbnail_url}")
        print(f"View Count: {self.view_count}")
        print(f"Subscriber Count: {self.subscriber_count}")
        print(f"Video Count: {self.video_count}")

    @property
    def url(self):
        """Возвращает ссылку на канал."""
        return f"https://www.youtube.com/channel/{self.__channel_id}"

    @staticmethod
    def get_service():
        """Возвращает объект для работы с YouTube API."""
        return Channel.youtube

    def to_json(self, filename: str) -> None:
        """Сохраняет информацию о канале в JSON-файл."""
        data = {
            'title': self.title,
            'description': self.description,
            'custom_url': self.custom_url,
            'published_at': self.published_at,
            'thumbnail_url': self.thumbnail_url,
            'view_count': self.view_count,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count
        }
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
