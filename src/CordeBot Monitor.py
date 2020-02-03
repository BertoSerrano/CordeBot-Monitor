import os
import time
from datetime import datetime
import cv2
import sys

original_stdout = sys.stdout
sys.stdout = None

SAVER_TIMER = 25  # Seconds to save a new image.

parent_folder = os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
with open(os.path.join(parent_folder, "etc", "config"), "r") as f:
    address = str(f.readline())
address.replace("\n", "")


def mkdirs(current_path, paths):
    """
    Creates folders in order to save the image files, json files and other necessary stuff
    :param current_path: parent folder where the script starts to make directories
    :param paths: collections of folder's names to create them recursively
    :return: the resulting path after the creations
    """
    current_path = os.path.join(current_path, str(paths[0]))
    if not os.path.exists(current_path):
        os.mkdir(current_path)
    return mkdirs(current_path, paths[1:]) if len(paths) > 1 else current_path


def save(current, frame):
    date = current.strftime("%m_%d_%Y")
    filename = str(os.path.join(mkdirs(parent_folder, ("savings", date)), str(current.strftime("%H_%M_%S")))) + ".png"
    cv2.imwrite(filename=filename, img=frame)


camera = cv2.VideoCapture("rtsp://{}".format(address))
errors = 0
last = datetime.now()
counter = 0

if camera.isOpened():

    while errors < 14:
        counter += 1
        if counter == 12:
            sys.stdout = original_stdout
            print("CordeBot Monitor Initiated")
        try:
            ret, frame = camera.read()
            errors -= 1 if errors > 0 else 0
            # cv2.imshow("CordeBot Monitor", frame)
            current = datetime.now()
            timer = current - last

            if timer.seconds > SAVER_TIMER:
                save(current, frame)
                last = current
        except:
            errors += 1
            print("ERROR: No frame arrived")

        # time.sleep(0.5)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
else:
    print("ERROR MESSAGE: The Foscam Camera is not opened")
camera.release()
cv2.destroyAllWindows()
print("CordeBot Monitor Closed")
