import os

print(list(filter(lambda x: os.path.isdir(f"./{x}"), os.listdir('.'))))