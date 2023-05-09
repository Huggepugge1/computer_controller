import pyautogui as pag
import time
import pytesseract
import gtts
from playsound import playsound
import threading
import os


class ImageToAudio(threading.Thread):
    def __init__(self, img):
        threading.Thread.__init__(self)
        self.img = img
        self.img = self.img.resize((self.img.size[0] * 3, self.img.size[1] * 3))
        self.img.save('./screen.png')
    
    def run(self):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
        text = pytesseract.image_to_string(self.img)

        if text == '' or text == '\n':
            text = 'Could not get song name'

        tts = gtts.gTTS(text)
        filename = './song_name.mp3'
        tts.save(filename)
         
        sound_thread = PlaySound(filename)
        sound_thread.start()

        print(self.img.size)


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

    
    def play(self, song_name=''):
        if song_name != '':
            pag.hotkey('ctrl', 'k')
            pag.press(map(lambda x: 'space' if x == ' ' else x, (c for c in song_name)))
            time.sleep(0.4)
            pag.hotkey('shift', 'enter')
            pag.press('esc')
        
        else:
            time.sleep(0.2)
            if pag.locateOnScreen('./spotify/images/play_button.png') is not None:
                pag.press('space')

    
    def pause(self):
        time.sleep(0.2)
        if pag.locateOnScreen('./spotify/images/pause_button.png') is not None:
            pag.press('space')

    
    def next_song(self):
        pag.hotkey('ctrl', 'right')


    def last_song(self):
        pag.hotkey('ctrl', 'left')
        pag.hotkey('ctrl', 'left')


    def get_repeat_status(self):
        time.sleep(0.2)
        if pag.locateOnScreen('./spotify/images/repeat_playlist.png') is not None:
            return 1
        elif pag.locateOnScreen('./spotify/images/repeat_song.png') is not None:
            return 2
        elif pag.locateOnScreen('./spotify/images/no_repeat.png') is not None:
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


    def song_name(self):
        pag.hotkey('win', 'up')
        time.sleep(0.2)
        heart_location = pag.locateOnScreen('./spotify/images/like.png').left
        heart_offset = 20
        img = pag.screenshot(region=(10, 970, heart_location - heart_offset, 28))

        sound_thread = ImageToAudio(img)
        sound_thread.start()
 
        pag.hotkey('win', 'down')
    

    def artist_name(self):
        pag.hotkey('win', 'up')
        time.sleep(0.2)
        heart_location = pag.locateOnScreen('./spotify/images/like.png').left
        heart_offset = 20
        img = pag.screenshot(region=(10, 993, heart_location - heart_offset, 28))

        sound_thread = ImageToAudio(img)
        sound_thread.start()
 
        pag.hotkey('win', 'down')
