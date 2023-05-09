import spotify
import time

for i in range(100):
    with spotify.Spotify() as s:
        s.play('Olivia rodrigo')

    time.sleep(1)
