#!/usr/bin/env python3
import spotify
import windows
import speech_recognition as sr

if __name__ == '__main__':
    while True:
        r   = sr.Recognizer()
        mic = sr.Microphone(device_index=1)

        with mic as source:
            audio = r.listen(source)

        try:
            recognized = list(map(lambda x: x.lower(), r.recognize_google(audio).split()))
            print(recognized)

            if recognized[0] in ['spotify', 'butterfly']:
                with spotify.Spotify(" ".join(recognized[1:])) as s:
                    s.start()
            elif recognized[0] == 'windows':
                w = windows.Windows(recognized[1], *recognized[2:])
                w.start()
            sound_thread = spotify.PlaySound('./listening.mp3', remove=False)
            sound_thread.start()


        except sr.exceptions.UnknownValueError:
            pass
