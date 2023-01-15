from operation.db_wrapper import DBWrapper
from operation.sptfy_wrapper import SptfyWrapper
from util.logging import Logger


class Evaluator:
    def __init__(self, sp: SptfyWrapper, db: DBWrapper, logger: Logger):
        self.__logger = logger
        self.__db = db
        self.__spotify = sp

    def get_most_played(self, limit):
        return self.__db.get_most_played_uris(limit)

    def evaluate(self, pl_name, **kwargs):
        most_played = self.__db.get_most_played(**kwargs)
        self.__spotify.set_playlist(most_played, pl_name)
        self.__logger.log(f"EVAL Set playlist '{pl_name}'")

    def evaluate_all(self, pl_name, limit):
        most_played = self.get_most_played(limit)
        self.__spotify.set_playlist(most_played, pl_name)
        self.__logger.log(f"EVAL Set playlist '{pl_name}'")

    def evaluate_period(self, pl_name, days, limit):
        most_played = self.__db.get_most_played_in_period(days, limit)
        print(most_played)
        if len(most_played) < 5:
            return
        self.__spotify.set_playlist(most_played, pl_name)
        self.__logger.log(f"EVAL Set playlist '{pl_name}'")

    def evaluate_genres(self, pl_name, genres: list, limit):
        most_played = self.__db.get_most_played_by_genres(genres, limit)
        self.__spotify.set_playlist(most_played, pl_name)
        self.__logger.log(f"EVAL Set playlist '{pl_name}'")

    def evaluate_popularity_songs(self, pl_name, min_popularity, max_popularity, limit):
        most_played = self.__db.get_most_played_by_song_popularity(min_popularity, max_popularity, limit)
        self.__spotify.set_playlist(most_played, pl_name)
        self.__logger.log(f"EVAL Set playlist '{pl_name}'")
