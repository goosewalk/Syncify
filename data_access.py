import requests
import base64
import json


class SpotifyDataAccess:
    TOKEN_URL = "https://accounts.spotify.com/api/token"
    PLAYLISTS_URL = "https://api.spotify.com/v1/users/{user_id}/playlists"
    PLAYLIST_TRACKS_URL = "https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

    def __init__(self, access_token):
        self.access_token = access_token

    def fetch_playlists(self, user_id):
        url = self.PLAYLISTS_URL.format(user_id=user_id)
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # This raises an error if there is any, check SpotifyForDevelopers
        json_response = response.json()
        print(json.dumps(json_response, indent=1))  # Used for debugging
        return json_response.get("items", [])

    def fetch_tracks(self, playlist_id):
        url = self.PLAYLIST_TRACKS_URL.format(playlist_id=playlist_id)
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error if the request fails

        json_response = response.json()
        tracks = json_response.get("items", [])  # Get the list of track items
        return tracks

    def get_access_token(client_id, client_secret):
        auth = f"{client_id}:{client_secret}"
        encoded_auth = base64.b64encode(auth.encode()).decode()  # Turn auth into bytes, encode with base64

        headers = {
            "Authorization": f"Basic {encoded_auth}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}

        response = requests.post(SpotifyDataAccess.TOKEN_URL, headers=headers, data=data)
        response.raise_for_status()
        return response.json()["access_token"]


if __name__ == "__main__":
    CLIENT_ID = "ID"
    CLIENT_SECRET = "SECRET"
    USER_ID = "s58hxm3raw4yd4kjssb6e1ihh"  # Profile ID from spotify i.e. https://open.spotify.com/user/{ID}

    try:
        access_token = SpotifyDataAccess.get_access_token(CLIENT_ID, CLIENT_SECRET)

        # Create DAO with the retrieved access token
        spotify = SpotifyDataAccess(access_token)

        # Fetch and print the user's public playlists
        playlists = spotify.fetch_playlists(USER_ID)

        print("Your Playlists:")
        for playlist in playlists:
            playlist_name = playlist['name']
            playlist_id = playlist['id']

            print(playlist_name)
            print("Tracks in Playlist:")

            # Fetch and print the tracks from the playlist
            tracks = spotify.fetch_tracks(playlist_id)
            for track in tracks:
                track_info = track.get("track")
                track_name = track_info.get("name")
                artist_name = track_info.get("artists")[0].get("name")
                print(f"- {track_name} by {artist_name}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
