import re
from providers.moviedata.provider import MoviedataProvider
from application import ACCESS_KEYS, APPLICATION as APP
try:
    from urllib import urlencode  # Python 2.X
except ImportError:
    from urllib.parse import urlencode  # Python 3+

IDENTIFIER = "theimdbapi"

class Provider(MoviedataProvider):
    def get_url(self, movie):
        parameters = {
            "title": movie["name"].encode("utf-8"),
        }
        if "year" in movie and movie["year"]:
            parameters["year"] = movie["year"]

        return "http://www.theimdbapi.org/api/find/movie?" + urlencode(parameters)

    def fetch_movie_data(self, movie):
        url = self.get_url(movie)
        APP.debug("Fetching url: %s" % url)
        data = self.parse_json(url)
        if not data:
            return {}

        for hit in data:
            # Return the first hit with a release date
            if hit and "release_date" in hit and hit["release_date"]:
                return self.transform_data(hit)

        return {}

    def get_data_mapping(self):
        return {
            "id": "imdb_id",
            "title": "title",
            "plot": "storyline",
            "genre": "genre",
            "director": "director",
            "country": "metadata.countries",
            "language": "metadata.languages",
            "runtime": "length",
            "released": "release_date",
            "age_rating": "content_rating",
            "year": "year",
            "imdb_url": "url",
            "imdb_poster": "poster.large",
            "imdb_rating": "rating",
            "imdb_rating_count": "rating_count",
        }
