import vk_api
from bs4 import BeautifulSoup
import requests
import os
import uuid
import shutil
from enum import Enum, auto

class Parser:
    class UrlType(Enum):
        VIDEO = auto()
        PHOTO = auto()

    def __init__(self, service_key):  
        vk_session = vk_api.VkApi(token=service_key)
        self.vk = vk_session.get_api()

    def process_player_link(self, player_link) -> None:
        soup = BeautifulSoup(player_link, 'html.parser')
        print(soup.video.find_all('source'))
        url =  soup.video.find_all('source')[1]["src"]
        if url.find('?') == -1:
            return url
        return url[:url.find('?')]


    def parse_video(self, video_obj):
        video = self.vk.video.get(videos=f"{video_obj['owner_id']}_{video_obj['id']}_{video_obj['access_key']}")
        return self.process_player_link(
            requests.get(video["items"][0]["player"]).content)

    def parse_photo(self, photo):
        return photo["sizes"][-1]["url"]

    def parse_attachments(self, attachments):
        urls = []
        for obj in attachments:
            if obj["type"] == "photo":
                urls.append([self.parse_photo(obj["photo"]),
                             self.UrlType.PHOTO])
            elif obj["type"] == "video":
                urls.append([self.parse_video(obj["video"]),
                             self.UrlType.VIDEO])
        return urls

    def process_id(self, wall_id):
        print("I am in process_id")
        try:
            obj = self.vk.wall.getById(posts=wall_id, fields="attachments")
            urls = self.parse_attachments(obj[0]["attachments"])
            return urls
        except Exception as exception:
            print(exception)
            return

    def parse_link(self, link):
        index = link.find("wall")
        if index == -1:
            return
        print(index)
        urls = self.process_id(link[index + 4:])
        return urls

