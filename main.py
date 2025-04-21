from time import time, sleep
import numpy as np
import shutil
import cv2
import sys
import os

def process(frameRaw):
    # ANSI colours
    ansi = [(12,12,12),
            (197,15,31),
            (19,161,14),
            (193,156,0),
            (0,55,218),
            (136,23,152),
            (58,150,221),
            (204,204,204)]

    # Easier to map 1D data that auto has luminance and rgb
    for f in (0.75, 0.5, 0.25):
        for a in ansi[:8]:
            ansi.append((int(a[0]*f), int(a[1]*f), int(a[2]*f)))

    # Get current terminal size, incase resized
    size = shutil.get_terminal_size()
    w, h = size.columns, size.lines
    y, x = frameRaw.shape[:2]

    frame = cv2.resize(frameRaw, (max(1, int(x*min(w/x, h/y))), max(1, int(y*min(w/x, h/y)))))

    # Update frame dimensions
    y, x = frame.shape[:2]

    # Map to ansi data
    pix = frame.reshape(-1, 3).astype(np.int32)
    ansi_arr = np.array(ansi, dtype=np.int32)
    diffs = pix[:, None, :] - ansi_arr[None, :, :]
    d_sqr = np.sum(diffs ** 2, axis=2)
    index = np.argmin(d_sqr, axis=1)

    output = []

    for i in range(y):
        row = []
        for j in range(x):
            row.append(f'\033[3{index[i*x+j]%8}m'+'█▓▒░'[index[i*x+j]//8])
        output.append(''.join(row) + '\033[0m')
    
    sys.stdout.write('\n'.join(output) + '\n')
    sys.stdout.flush()

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

    FPS = cap.get(cv2.CAP_PROP_FPS)

    try:
        # Enter a loop to read frames and process them one by one
        while 1:
            start = time()

            valid, frame = cap.read()

            # End of video
            if not valid:
                break

            # Actual conversion happens here
            process(frame)

            # Allign with FPS, skip frames if over
            if time()-start > 1/FPS:
                for i in range(round((time()-start)*FPS) - 1):
                    cap.read()
            else:
                while time()-start < 1/FPS:
                    sleep(0.01/FPS)

    # User can manually exit
    except KeyboardInterrupt:
        pass

    # I do not trust the garbage collector
    finally:
        cap.release()