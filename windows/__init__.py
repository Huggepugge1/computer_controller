import os
import sys
import threading

sys.setrecursionlimit(int(2**31 - 1))

PATH = [
    r'C:\Windows',
    r'C:\"Program Files"',
    r'C:\"Program Files (x86)"',
    r'C:\Users\hugge\AppData\Local\Programs',
    r'C:\Users\hugge\AppData\Local',
    r'D:\"Program Files"',
    r'D:\"Program Files (x86)"'
]


def get_paths(depth, p):
    if depth == 1:
        try:
            return list(map(lambda x: x if x.count(' ') == 0 else rf'"{x}"', filter(lambda x: os.path.isdir(rf'{p}\{x}'), os.listdir(p))))
        except PermissionError:
            return None
    paths = []
    try:
        for path in filter(lambda x: os.path.isdir(rf'{p}\{x}'), os.listdir(p)):
            next_level = get_paths(depth - 1, rf'{p}\{path}')
            if next_level is None:
                continue
            for i in list(map(lambda x: rf'{path}\{x}' if x.count(' ') == 0 else rf'{path}\"{x}"', next_level)):
                paths.append(i)
    except PermissionError:
        return None

    return paths


class Windows(threading.Thread):
    def __init__(self, func, *argv):
        self.func = func
        self.argv = argv
        threading.Thread.__init__(self)

    def open(self):
        app = " ".join(self.argv)
        for p in PATH:
            striped_p = p.replace('"', '')
            if os.path.isfile(rf'{striped_p}\{app}.exe'):
                os.system(rf'start {p}\"{app}"')
                return
            elif os.path.isfile(rf'{striped_p}\{app}\{app}.exe'):
                os.system(rf'start {p}\"{app}"\"{app}"')
                return
            elif os.path.isfile(rf'{striped_p}\application\{app}.exe'):
                os.system(rf'start {p}\application\"{app}"')
                return

        for i in range(1, 4):
            for p1 in PATH:
                for p2 in get_paths(i, p1.replace('"', '')):
                    striped_p = rf'{p1}\{p2}'.replace('"', '')
                    if os.path.isfile(rf'{striped_p}\{app}.exe'):
                        os.system(rf'start {p1}\{p2}\"{app}"')
                        return
                    elif os.path.isfile(rf'{striped_p}\{app}\{app}.exe'):
                        os.system(rf'start {p1}\{p2}\"{app}"\"{app}"')
                        return
                    elif os.path.isfile(rf'{striped_p}\application\{app}.exe'):
                        os.system(rf'start {p1}\{p2}\application\"{app}"')
                        return

    def run(self):
        if self.func in ['open', 'run', 'around']:
            self.open()
        return
