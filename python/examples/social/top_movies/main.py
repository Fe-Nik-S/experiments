
import imdb


SHOWED_MOVIES_COUNT = 20

if __name__ == "__main__":
    imdb_client = imdb.IMDb()
    top_movies = imdb_client.get_top250_movies()
    print("TOP-{}:".format(SHOWED_MOVIES_COUNT))
    for movie in top_movies[:SHOWED_MOVIES_COUNT]:
        print(movie)
