import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
import json
from sentence_transformers import SentenceTransformer
import numpy as np


def get_albums():
    load_dotenv()
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    credentials = SpotifyClientCredentials(client_id, client_secret)
    spotify = spotipy.Spotify(client_credentials_manager=credentials)
    artist_uris = [
        "spotify:artist:5gQB07Vco4zBCUNbf8SBx4",
        "spotify:artist:6uaBJl3pf08WJd63jQ5HaW",
        "spotify:artist:1SHuwxHlrs4sxReozrn80W",
    ]

    albums = []
    for artist_uri in artist_uris:
        results = spotify.artist_albums(artist_uri, album_type="album")
        while results["next"]:
            results = spotify.next(results)
            albums.extend(results["items"])

    with open("albums.json", "w") as f:
        f.write(json.dumps(albums))

    return albums


def compute_embeddings(albums):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode([d["name"] for d in albums], convert_to_tensor=True)
    np.save("embeddings.npy", embeddings)


if __name__ == "__main__":
    albums = get_albums()
    compute_embeddings(albums)
