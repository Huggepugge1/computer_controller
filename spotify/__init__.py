import pyautogui as pag
import time
import pytesseract
import gtts
from playsound import playsound
import threading
import os
import speech_recognition as sr


class ImageToAudio(threading.Thread):
    def __init__(self, img):
        threading.Thread.__init__(self)
        self.img = img
    

    def run(self):
        scale = 10
        self.img = self.img.resize((self.img.size[0] * scale, self.img.size[1] * scale))
        self.img.save("save.png")
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
        text = pytesseract.image_to_string(self.img)

        if text == '' or text == '\n':
            text = 'Could not get song name'

        tts = gtts.gTTS(text)
        filename = './song_name.mp3'
        tts.save(filename)
         
        sound_thread = PlaySound(filename)
        sound_thread.start()


class PlaySound(threading.Thread):
    def __init__(self, sound_file):
        threading.Thread.__init__(self)
        self.sound_file = sound_file

    def run(self):
        playsound(self.sound_file)
        os.remove(self.sound_file)


class Spotify:
    def __enter__(self):
        pag.press('win')
        pag.press(c for c in 'spotify')
        pag.press('enter')
        return self


    def __exit__(self, type, value, traceback):
        pag.hotkey('win', 'down')
        return False

    
    def play(self):
        time.sleep(0.2)
        if pag.locateOnScreen('./spotify/images/play_button.png', confidence=.95) is not None:
            pag.press('space')
        else:
            r   = sr.Recognizer()
            mic = sr.Microphone(device_index=1)

            with mic as source:
                audio = r.listen(source, 1000000, 4)

            try:
                song_name = ' '.join(map(lambda x: x.lower(), r.recognize_google(audio).split()))
                print(list(map(lambda x: 'space' if x == ' ' else x, (c for c in song_name))))
                pag.hotkey('ctrl', 'k')
                pag.press(map(lambda x: 'space' if x == ' ' else x, (c for c in song_name)))
                time.sleep(0.4)
                pag.hotkey('shift', 'enter')
                pag.press('esc')

            except sr.exceptions.UnknownValueError:
                pass

    
    def pause(self):
        time.sleep(0.2)
        if pag.locateOnScreen('./spotify/images/pause_button.png', confidence=.95) is not None:
            pag.press('space')

    
    def next_song(self):
        pag.hotkey('ctrl', 'right')


    def last_song(self):
        pag.hotkey('ctrl', 'left')
        pag.hotkey('ctrl', 'left')


    def get_repeat_status(self):
        time.sleep(0.2)
        if pag.locateOnScreen('./spotify/images/repeat_playlist.png', confidence=.90) is not None:
            return 1
        elif pag.locateOnScreen('./spotify/images/repeat_song.png', confidence=.90) is not None:
            return 2
        elif pag.locateOnScreen('./spotify/images/no_repeat.png', confidence=.90) is not None:
            return 0
    
    
    def no_repeat(self):
        for i in range((0 - self.get_repeat_status()) % 3):
            pag.hotkey('ctrl', 'r')
        

    def repeat_playlist(self):
        for i in range((1 - self.get_repeat_status()) % 3):
            pag.hotkey('ctrl', 'r')


    def repeat_song(self):
        for i in range((2 - self.get_repeat_status()) % 3):
            pag.hotkey('ctrl', 'r')
    

    def shuffle(self):
        time.sleep(0.2)
        if pag.locateOnScreen('./spotify/images/shuffle.png', confidence=.90) is None:
            pag.hotkey('ctrl', 's')


    def stop_shuffle(self):
            time.sleep(0.2)
            if pag.locateOnScreen('./spotify/images/dont_shuffle.png', confidence=.90) is None:
                pag.hotkey('ctrl', 's')


    def song_name(self):
        pag.hotkey('win', 'up')
        time.sleep(0.2)
        pag.click(pag.locateCenterOnScreen('./spotify/images/home.png', confidence=.90))
        heart_location = pag.locateOnScreen('./spotify/images/like.png', confidence=.90).left
        heart_offset = 20
        img = pag.screenshot(region=(10, 970, heart_location - heart_offset, 28))

        sound_thread = ImageToAudio(img)
        sound_thread.start()
 
        pag.hotkey('win', 'down')
    

    def artist_name(self):
        pag.hotkey('win', 'up')
        time.sleep(0.2)
        pag.click(pag.locateCenterOnScreen('./spotify/images/home.png', confidence=.90))
        heart_location = pag.locateOnScreen('./spotify/images/like.png', confidence=.90).left
        heart_offset = 20
        img = pag.screenshot(region=(10, 993, heart_location - heart_offset, 28))

        sound_thread = ImageToAudio(img)
        sound_thread.start()
 
        pag.hotkey('win', 'down')


    def playlist_information(self):
        time.sleep(0.2)
        pag.click(pag.locateCenterOnScreen('./spotify/images/home.png', confidence=.90))
        pag.hotkey('win', 'up')
        pag.hotkey('alt', 'shift', 'j')
        time.sleep(0.2)
        img = pag.screenshot('save.png', region=(550, 170, 1350, 250))

        sound_thread = ImageToAudio(img)
        sound_thread.start()
 
        pag.hotkey('win', 'down')
