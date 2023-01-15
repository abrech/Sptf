import requests

from operation.db_wrapper import DBWrapper
from operation.sptfy_wrapper import SptfyWrapper
from util.logging import Logger


class SongCollector:
    def __init__(self, spotify: SptfyWrapper, database: DBWrapper, logger: Logger, min_time_played):
        self.__logger = logger
        self.__spotify = spotify
        self.__db = database
        self.__min_time_played = min_time_played * 1000
        self.__previous_uri = None

    def collect(self, retries=2):
        try:
            song_obj = self.__spotify.get_song_info()
            artist_obj = self.__spotify.get_artist_info(song_obj.artist_uri)
            self.__logger.log(f"COLL collected {song_obj.song} by {artist_obj.name}")
        except requests.exceptions.ReadTimeout:
            self.__logger.log("COLL ReadTimeout Exception occured while collecting", level=1)
            if retries > 0:
                self.collect(retries - 1)
                return
            else:
                return

        if not song_obj.uri or song_obj.uri == self.__previous_uri:
            return

        self.__previous_uri = song_obj.uri

        self.__db.add_artist(artist_obj)
        self.__db.add_song(song_obj)

        self.__logger.log(f"COLL {song_obj.song} by {artist_obj.name}")

    def run(self):
        ms = self.__spotify.get_ms()
        if ms and ms > self.__min_time_played:
            self.collect()
        elif not ms:
            self.__spotify.update_device()
