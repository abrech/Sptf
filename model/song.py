class Song:
    def __init__(self, song, artist, uri, artist_uri, album, popularity, duration, img_src):
        self.song = song
        self.artist = artist
        self.uri = uri
        self.artist_uri = artist_uri
        self.album = album
        self.popularity = popularity
        self.duration = duration
        self.img_src = img_src

    def __str__(self) -> str:
        return f"{self.song} by {self.artist}"

