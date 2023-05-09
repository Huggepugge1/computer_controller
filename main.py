#!/usr/bin/env python3
import spotify
import speech_recognition as sr

if __name__ == '__main__':
    
    r   = sr.Recognizer()
    mic = sr.Microphone(device_index=1)
    
    while True:
        with mic as source:
            audio = r.listen(source, 1000000, 5)

        try:
            recognized = r.recognize_google(audio).split()
            print(recognized)
            
            if len(recognized) >= 2:
                if recognized[0] == 'Spotify':
                    with spotify.Spotify() as s:
                        if recognized[1] == 'play':
                            if len(recognized) == 2:
                                s.play()
                            else:
                                s.play(' '.join(recognized[2:]))
                        elif recognized[1] == 'pulse' or recognized[1] == 'post' or recognized[1] == 'pause':
                            s.pause()
                        elif recognized[1] == 'next':
                            s.next_song()
                        elif recognized[1] == 'last':
                            s.last_song()
                        elif len(recognized) == 3:
                            if recognized[1] == 'repeat':
                                if recognized[2] == 'stop':
                                    s.no_repeat()
                                elif recognized[2] == 'song':
                                    s.repeat_song()
                                elif recognized[2] == 'playlist':
                                    s.repeat_playlist()
                            elif 'name' in recognized[1]:
                                if recognized[2] == 'song':
                                    s.song_name()
                                elif recognized[2] == 'artist':
                                    s.artist_name()

        except sr.exceptions.UnknownValueError:
            pass
