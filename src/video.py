from datetime import datetime

from src.channel import Channel


class Video:
    """Класс для ютуб-канала"""

    def __init__(self, video_id: str):
        self.video_id = video_id
        self.video_title = None
        self.published_at = None
        self.view_count = None
        self.like_count = None
        self.comment_count = None

        if video_id:
            try:
                self.get_video_info()
            except Exception as e:
                print(f"Произошла ошибка при получении информации о видео: {e}.")

    def __str__(self) -> str:
        return self.video_title

    def get_video_info(self):
        video_response = Channel.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                             id=self.video_id
                                                             ).execute()

        if 'items' in video_response and video_response['items']:
            video = video_response['items'][0]
            snippet = video['snippet']
            statistics = video['statistics']

            self.video_title = snippet['title']
            self.published_at = datetime.strptime(snippet['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
            self.view_count = int(statistics['viewCount'])
            self.like_count = int(statistics.get('likeCount', 0))
            self.comment_count = int(statistics.get('commentCount', 0))


class PLVideo(Video):
    """Класс для плейлиста"""

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
