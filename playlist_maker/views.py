from django.shortcuts import render, redirect
import spotipy
import spotipy.util as util

# Create your views here.

SPOTIPY_CLIENT_ID = "1091e4ae6b354e14b4c556f1f1a6732c"
SPOTIPY_CLIENT_SECRET = "8d9f32269887450f99cd7bd106a6c3d4"
SPOTIPY_REDIRECT_URI = "http://localhost:8000/"
scope = "playlist-modify-public"
username = "ttbriyo504kilcgb12zr3tf6g"
token = util.prompt_for_user_token(username, scope, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)
sp = spotipy.Spotify(auth=token)

def index(request):
    return render(request, 'playlist_maker/index.html')

def artist_not_found(request):
    return render(request, 'playlist_maker/artist_not_found.html')


def show_playlist(request):
    if request.method == 'GET':
        desired_artist = request.GET.get("artist_to_search")
    if not desired_artist:
        return redirect('playlist_maker:index')
    desired_artist_results = sp.search(q="artist:" + desired_artist, type="artist")
    if len(desired_artist_results["artists"]["items"]) == 0:
        return redirect('playlist_maker:artist_not_found')

    desired_artist_entry = desired_artist_results["artists"]["items"][0]
    artist_name = desired_artist_entry["name"]
    artist_uri = desired_artist_entry["uri"]
    artist_image_url = desired_artist_entry["images"][0]["url"]

    playlist_name = "Inspired by " + artist_name
    sp.trace = False
    playlist = sp.user_playlist_create(username, playlist_name)
    playlist_id = playlist["id"]

    list_of_tracks = []

    artist_top_tracks = sp.artist_top_tracks(artist_uri)
    song_count = 0
    for track in artist_top_tracks["tracks"]:
        if song_count < 5:
            list_of_tracks.append(track["id"])
            song_count += 1

    add_tracks_to_playlist = sp.user_playlist_add_tracks(username, playlist_id, list_of_tracks)
    playlist_iframe_href = "https://open.spotify.com/embed?uri=spotify:user:" + username + ":playlist:" + playlist_id + "&theme=white"
    
    context = {
        'artist_name':artist_name,
        'image' :artist_image_url,
        'frame' :playlist_iframe_href 
    }

    return render(request, 'playlist_maker/playlist.html', context)