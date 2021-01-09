import cv2
import numpy as np
import os

if __name__ == "__main__":
    KNOWN_FACES_DIR = "known_faces"
    known_names = []
    name = ""

    # load names that are already there
    for name in os.listdir(KNOWN_FACES_DIR):
        known_names.append(name)

    # ask user for name
    print("input your name")
    name = input()

    # make sure name is unique
    while name != "" and name in known_names:
        print("The name: " + name + " is taken please chose another name")
        name = input()

    # capture video
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        # Get frame and show it
        ret, frame = cap.read()
        cv2.imshow("New User", frame)

        # if you press q close the window
        # Also creates a new Directory for User
        if cv2.waitKey(1) % 0xFF == ord("q"):
            new_dir = KNOWN_FACES_DIR + f"\{name}"
            new_pic = new_dir + f"\{name}" + ".jpg"
            os.mkdir(new_dir)
            cv2.imwrite(new_pic, frame)

            break

    cap.release()
    cv2.destroyAllWindows()
