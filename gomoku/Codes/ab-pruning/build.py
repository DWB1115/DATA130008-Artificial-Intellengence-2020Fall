import os

THRESHOLD = 7  # search depth
DEPTH = 11  # checkmate depth
branch = [8, 6, 4, 3, 3, 3, 3, 4, 3]
BRUNCH = 6  # checkmate brunch
DIST = 1
CHECK_DIST = 1
RATIO = 0.1

if __name__ == '__main__':
    os.system("pyinstaller pbrain.py pisqpipe.py --name pbrain-ab-pruning.exe --onefile")

