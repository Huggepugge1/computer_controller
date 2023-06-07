import gtts
from playsound import playsound
import threading
import os
import speech_recognition as sr
import spotipy
import spotipy.util as util
from pprint import pprint


class TextToAudio(threading.Thread):
    def __init__(self, text):
        threading.Thread.__init__(self)
        self.text = text

    def run(self):
        tts = gtts.gTTS(self.text)
        filename = './track_name.mp3'
        tts.save(filename)

        sound_thread = PlaySound(filename)
        sound_thread.start()


class PlaySound(threading.Thread):
    def __init__(self, sound_file, remove=True):
        threading.Thread.__init__(self)
        self.sound_file = sound_file
        self.remove = remove

    def run(self):
        playsound(self.sound_file)
        if self.remove:
            os.remove(self.sound_file)


class Spotify(threading.Thread):
    def __init__(self, func):
        self.func = func
        threading.Thread.__init__(self)

    def __enter__(self):
        username = "o2qkd20qrvolzmi4mdgrs4s37"

        scope = "user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control " \
                "streaming playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public " \
                "user-read-playback-position user-top-read user-read-recently-played user-library-read "
        try:
            token = util.prompt_for_user_token(username, scope)
        except:
            os.remove(f".cache-{username}")
            token = util.prompt_for_user_token(username, scope)
        self.sp = spotipy.Spotify(auth=token)
        return self

    def __exit__(self, type, value, traceback):
        return False

    def play(self):
        try:
            self.sp.start_playback()
        except spotipy.exceptions.SpotifyException:
            pass
        return

    def pause(self):
        self.sp.pause_playback()
        return

    def next_track(self):
        self.sp.next_track()
        return

    def last_track(self):
        self.sp.previous_track()
        return

    def no_repeat(self):
        self.sp.repeat("off")
        return

    def repeat_playlist(self):
        self.sp.repeat("context")
        return

    def repeat_track(self):
        self.sp.repeat("track")
        return

    def shuffle(self):
        self.sp.shuffle(True)
        return

    def stop_shuffle(self):
        self.sp.shuffle(False)
        return

    def track_name(self):
        sound_thread = TextToAudio(self.sp.current_playback()['item']['name'])
        sound_thread.start()
        return

    def artist_name(self):
        artists = []
        for artist in self.sp.current_playback()['item']['artists']:
            artists.append(artist["name"])
        sound_thread = TextToAudio(" and ".join(artists))
        sound_thread.start()
        return

    def track_info(self):
        track = self.sp.current_playback()
        context = track['context']
        print(context)

        if context is None:
            artists = []
            for artist in track['item']['album']['artists']:
                artists.append(artist["name"])
            sound_thread = TextToAudio(f'You are listening to {track["item"]["name"]} by {" and ".join(artists)}.')
            sound_thread.start()

        elif context['type'] == 'album':
            artists = []
            for artist in track['item']['album']['artists']:
                artists.append(artist["name"])
            if track['item']['album']['album_type'] == 'single':
                sound_thread = TextToAudio(f'You are listening to a {track["item"]["album"]["album_type"]}'
                                           f'called {track["item"]["album"]["name"]} by {" and ".join(artists)}.')
            else:
                sound_thread = TextToAudio(f'You are listening to a {track["item"]["album"]["album_type"]}'
                                           f'called {track["item"]["album"]["name"]} by {" and ".join(artists)}.'
                                           f'Current track: {track["item"]["name"]}')
            sound_thread.start()

        elif context['type'] == 'artist':
            artists = []
            for artist in track['item']['artists']:
                artists.append(artist["name"])
            sound_thread = TextToAudio(f'You are listening to {self.sp.artists([context["uri"]])["artists"][0]["name"]}.'
                                       f'Current track: {track["item"]["name"]} by {" and ".join(artists)}')
            sound_thread.start()

        elif context['type'] == 'playlist':
            artists = []
            for artist in track['item']['artists']:
                artists.append(artist["name"])
            sound_thread = TextToAudio(f'You are listening to {self.sp.playlist(context["uri"])["name"]}. '
                                       f'Current track: {track["item"]["name"]} by {" and ".join(artists)}')
            sound_thread.start()

    def search(self, q):
        if q[0].lower() == 'track':
            self.sp.start_playback(uris=[
                self.sp.search(" ".join(q[1:]), 1, 0, type='track'.lower())['tracks']['items'][0]['uri']])
        elif q[0].lower() in ['artist', 'album', 'playlist']:
            self.sp.start_playback(context_uri=
                                   self.sp.search(" ".join(q[1:]), 1, 0, type=q[0].lower())[
                                       q[0].lower() + 's']['items'][0]['uri'])

    def run(self):
        func = self.func
        if func == 'play':
            self.play()
        elif func in ['pause', 'pulse']:
            self.pause()
        elif func in ['next', 'next song', 'next track']:
            self.next_track()
        elif func in ['last', 'last song', 'last track']:
            self.last_track()
        elif func == 'no_repeat':
            self.no_repeat()
        elif func == 'repeat playlist':
            self.repeat_playlist()
        elif func == 'repeat track':
            self.repeat_track()
        elif func == 'shuffle':
            self.shuffle()
        elif func == 'don\'t shuffle':
            self.stop_shuffle()
        elif func == 'name track':
            self.track_name()
        elif func == 'name aritst':
            self.artist_name()
        elif func == 'track info':
            self.track_info()
        elif func.split()[0] == 'search':
            self.search(func.split()[1:])
        else:
            print("unknown command")
        return
