import shutil
import cv2
import sys
import os

# NOT USED YET
class colour:
    # turn 30m into 40m for highlight
    BLACK = '\033[30m' # (12,12,12)
    RED = '\033[31m' # (197,15,31)
    GREEN = '\033[32m' # (19,161,14)
    YELLOW = '\033[33m' # (193,156,0)
    BLUE = '\033[34m' # (0,55,218)
    PURPLE = '\033[35m' # (136,23,152)
    CYAN = '\033[36m' # (58,150,221)
    WHITE = '\033[37m' # (204,204,204)

def process(frameRaw):
    # Get current terminal size, incase resized
    size = shutil.get_terminal_size()
    w, h = size.columns, size.lines
    x, y = frameRaw.shape[:2]

    # Resize to fit in terminal with same aspect ratio
    if x/w > y/h:
        frame = cv2.resize(frameRaw, (w, int(w*y/x)))
    else:
        frame = cv2.resize(frameRaw, (int(h*x/y), h))

    # Update frame dimensions
    x, y = frame.shape[:2]

    # Cast to greyscale
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Go over the pixels and cast them
    out = ''
    for row in frame:
        for pixel in row:
            # Nested if statements are a crime, i know :(
            if pixel < 51:
                out += ' '
            elif pixel < 102:
                out += '░'
            elif pixel < 153:
                out += '▒'
            elif pixel < 204:
                out += '▓'
            else:
                out += '█'
        out += '\n'
    print(out)

if __name__ == '__main__':
    # If no args passed explain how to use
    if len(sys.argv) == 1:
        raise ValueError('Missing argument, no video file path was passed in')

    # If too many raise error
    if len(sys.argv) >= 3:
        raise ValueError('Too many arguments, only 1 video file path accepted')

    filepath = sys.argv[1]

    # File doesn't exist
    if not os.path.exists(filepath):
        raise ValueError('Invalid filepath, file doesnt exist')

    cap = cv2.VideoCapture(filepath)

    # Invalid file
    if not cap.isOpened():
        raise ValueError('Error, video could not be opened')

    try:
        # Enter a loop to read frames and process them one by one
        while 1:
            valid, frame = cap.read()

            # End of video
            if not valid:
                break

            # Actual conversion happens here
            process(frame)

    # User can manually exit
    except KeyboardInterrupt:
        pass

    # I do not trust the garbage collector
    finally:
        cap.release()