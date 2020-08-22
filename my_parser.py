import vk_api
from bs4 import BeautifulSoup
import requests
import os
import uuid
import shutil

class Parser:
    def __init__(self, service_key):  
        vk_session = vk_api.VkApi(token=service_key)
        self.vk = vk_session.get_api()

    def process_player_link(self, filename, player_link) -> None:
        soup = BeautifulSoup(player_link, 'html.parser')
        link = soup.video.find_all('source')[1]["src"]

        resp = requests.get(link)
        with open(filename, "wb") as f:
            f.write(resp.content)   


    def parse_video(self, video_obj, path):
        file_id = uuid.uuid4()
        video = self.vk.video.get(videos=f"{video_obj['owner_id']}_{video_obj['id']}_{video_obj['access_key']}")
        self.process_player_link(f"{path}\\{file_id}.mp4",
            requests.get(video["items"][0]["player"]).content)

    def parse_photo(self, photo, path):
        file_id = uuid.uuid4()
        url = photo[0]["sizes"][-1]["url"]
        with open(path + file_id + ".jpeg", "wb") as f:
            f.write(requests.get(url).content)

    def parse_attachments(self, attachments, path):
        for obj in attachments:
            if obj["type"] == "photo":
                self.parse_photo(obj["photo"], path)
            elif obj["type"] == "video":
                self.parse_video(obj["video"], path)

    def make_directory(self):
        dir_id = uuid.uuid4()
        path = f"{os.getcwd()}\\tmp{dir_id}"
        os.mkdir(path)
        return path
    
    def delete_directory(self, path):
        shutil.rmtree(path)

    def process_id(self, path, wall_id):
        print("I am in process_id")
        try:
            obj = self.vk.wall.getById(posts=wall_id, fields="attachments")
            self.parse_attachments(obj[0]["attachments"], path)
        except Exception as exception:
            print(exception)
            return

    def parse_link(self, link, path):
        index = link.find("wall")
        if index == -1:
            return
        print(index)
        self.process_id(path, link[index + 4:])

