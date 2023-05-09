#!/usr/bin/env python3
import spotify
import speech_recognition as sr

if __name__ == '__main__':
    
    r   = sr.Recognizer()
    mic = sr.Microphone(device_index=1)
    
    while True:
        with mic as source:
            audio = r.listen(source, 1000000, 3)

        try:
            recognized = list(map(lambda x: x.lower(), r.recognize_google(audio).split()))
            print(recognized)
            
            if len(recognized) >= 2:
                if recognized[0] == 'spotify':
                    with spotify.Spotify() as s:
                        if recognized[1] == 'play':
                            s.play()
                        elif recognized[1] == 'pulse' or recognized[1] == 'post' or recognized[1] == 'pause':
                            s.pause()
                        elif recognized[1] == 'next':
                            s.next_song()
                        elif recognized[1] == 'last':
                            s.last_song()
                        elif recognized[1] == 'shuffle':
                            s.shuffle()
                        elif len(recognized) == 3:
                            if recognized[1] == 'don\'t':
                                if recognized[2] == 'repeat':
                                    s.no_repeat()
                                elif recognized[2] == 'shuffle':
                                    s.stop_shuffle()
                            elif recognized[1] == 'repeat':
                                if recognized[2] == 'song':
                                    s.repeat_song()
                                elif recognized[2] == 'playlist':
                                    s.repeat_playlist()
                            elif 'name' in recognized[1]:
                                if recognized[2] == 'song':
                                    s.song_name()
                                elif recognized[2] == 'artist':
                                    s.artist_name()
                            elif recognized[1] == 'playlist':
                                if recognized[2] == 'information':
                                    s.playlist_information()

        except sr.exceptions.UnknownValueError:
            pass
