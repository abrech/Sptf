class Artist:
    def __init__(self, name, uri, popularity, genres: list) -> None:
        self.name = name
        self.uri = uri
        self.popularity = popularity
        self.genres = genres

    def __str__(self) -> str:
        return f"{self.name}"