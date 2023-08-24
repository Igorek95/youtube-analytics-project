import os
import isodate
import datetime
from googleapiclient.discovery import build


class PlayList:
    """
    Класс, представляющий плейлист на YouTube.

    Атрибуты:
        api_key (str): Ключ API YouTube из переменных окружения.
        youtube (googleapiclient.discovery.Resource): Клиент API YouTube.
        id (str): ID плейлиста.
        title (str): Название плейлиста.
        url (str): Ссылка на плейлист.

    Методы:
        __init__(self, _id_: str): Инициализирует экземпляр класса PlayList.
        get_playlist_info(self): Получает название и URL плейлиста.
        total_duration(self): Возвращает общую продолжительность всех видео в плейлисте.
        show_best_video(self): Возвращает ссылку на самое популярное видео в плейлисте.
    """
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, _id_: str):
        """
        Инициализация экземпляра класса PlayList.

        Аргументы:
            _id_ (str): ID плейлиста.
        """
        self.id = _id_
        self.title, self.url = self.get_playlist_info()

    def get_playlist_info(self):
        """
        Получает название и URL плейлиста.

        Возвращает:
            tuple: Кортеж, содержащий название и URL плейлиста.
        """
        playlist_response = self.youtube.playlists().list(
            id=self.id,
            part='snippet',
        ).execute()
        playlist = playlist_response['items'][0]['snippet']
        return playlist['title'], f"https://www.youtube.com/playlist?list={self.id}"

    @property
    def total_duration(self):
        """
        Возвращает общую продолжительность всех видео в плейлисте.
        """
        playlist_videos = self.youtube.playlistItems().list(
            playlistId=self.id,
            part='contentDetails',
            maxResults=50,
        ).execute()
        video_ids = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = self.youtube.videos().list(
            part='contentDetails',
            id=','.join(video_ids)
        ).execute()

        total_seconds = 0
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_seconds += duration.total_seconds()

        return datetime.timedelta(seconds=total_seconds)

    def show_best_video(self):
        """
        Возвращает:
            str: Ссылка на самое популярное видео, или None, если подходящего видео не найдено.
        """
        playlist_videos = self.youtube.playlistItems().list(
            playlistId=self.id,
            part='snippet',
            maxResults=50,
        ).execute()

        best_video_id = None
        max_likes = 0
        for video in playlist_videos['items']:
            video_id = video['snippet']['resourceId']['videoId']
            video_response = self.youtube.videos().list(
                part='statistics',
                id=video_id
            ).execute()

            like_count = int(video_response['items'][0]['statistics']['likeCount'])
            if like_count > max_likes:
                max_likes = like_count
                best_video_id = video_id

        if best_video_id:
            return f"https://youtu.be/{best_video_id}"
        else:
            return None
