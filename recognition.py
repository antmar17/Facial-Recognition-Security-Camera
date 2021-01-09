from send_msg import send_image_email
import cv2
import numpy as np
import os
import time
import face_recognition.api as FR

# iterate over unknown faces folder for testing
def test():
    # loop over unknown faces
    print("processing unknown faces")
    for filename in os.listdir(UNKNOWN_FACES_DIR):
        # load the image
        print(f"Filename {filename}", end="")
        image = FR.load_image_file(f"{UNKNOWN_FACES_DIR}/{filename}")

        # Find the location of the faces
        locations = FR.face_locations(image, model=MODEL)

        # pass locations to face_encodings to cut down on processing time
        encodings = FR.face_encodings(image, locations)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        print(f",found {len(encodings)} face(s)")

        for face_encoding, face_location in zip(encodings, locations):
            results = FR.compare_faces(known_faces, face_encoding, TOLERENCE)
            match = None

            if True in results:
                match = known_names[results.index(True)]
                print(f"Match Found {match}")
                # dimensions of where the face is
                top_left = (face_location[3], face_location[0])
                bottom_right = (face_location[1], face_location[2])

                # draw rectangle on image
                color = [0, 255, 0]
                cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)

                top_left = (face_location[3], face_location[0])
                bottom_right = (face_location[1], face_location[2] + 22)
                # cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)
                cv2.putText(
                    image,
                    match,
                    (face_location[3] + 10, face_location[2] + 15),
                    cv2.FONT_HERSHEY_COMPLEX,
                    0.5,
                    (200, 200, 200),
                    FONT_THICKNESS,
                )

        cv2.imshow(filename, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":

    KNOWN_FACES_DIR = "known_faces"
    UNKNOWN_FACES_DIR = "unknown_faces"
    FRAME_THICKNESS = 3
    FONT_THICKNESS = 2
    TOLERENCE = 0.6
    MODEL = "hog"

    known_faces = []
    known_names = []

    # loop over known faces
    print("loading faces")
    for name in os.listdir(KNOWN_FACES_DIR):
        for filename in os.listdir(f"{KNOWN_FACES_DIR}/{name}"):
            image = FR.load_image_file(f"{KNOWN_FACES_DIR}/{name}/{filename}")
            encoding = FR.face_encodings(image)[0]
            known_faces.append(encoding)
            known_names.append(name)
    print("faces loaded!")
    print("starting camera")
    # record
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FPS, 30)

    while True:
        ret, frame = cap.read()
        frame = np.array(frame)

        locations = FR.face_locations(frame, model=MODEL)
        encodings = FR.face_encodings(frame, locations)
        print(f"found {len(encodings)} face(s)")

        for face_encoding, face_location in zip(encodings, locations):
            results = FR.compare_faces(known_faces, face_encoding, TOLERENCE)
            match = None
            if True in results:
                match = known_names[results.index(True)]
                print(f"Match Found {match}")
                # dimensions of where the face is
                top_left = (face_location[3], face_location[0])
                bottom_right = (face_location[1], face_location[2])

                # draw rectangle on image
                color = [0, 255, 0]
                cv2.rectangle(frame, top_left, bottom_right, color, FRAME_THICKNESS)

                top_left = (face_location[3], face_location[0])
                bottom_right = (face_location[1], face_location[2] + 22)
                # cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)
                cv2.putText(
                    frame,
                    match,
                    (face_location[3] + 10, face_location[2] + 15),
                    cv2.FONT_HERSHEY_COMPLEX,
                    0.5,
                    (200, 200, 200),
                    FONT_THICKNESS,
                )

            else:
                match = "Unknown"
                color = [255, 0, 0]
                top_left = (face_location[3], face_location[0])
                bottom_right = (face_location[1], face_location[2])
                cv2.rectangle(frame, top_left, bottom_right, color, FRAME_THICKNESS)

                cv2.putText(
                    frame,
                    match,
                    (face_location[3] + 10, face_location[2] + 15),
                    cv2.FONT_HERSHEY_COMPLEX,
                    0.5,
                    (200, 200, 200),
                    FONT_THICKNESS,
                )
                # alert the Owner of the computer
                cv2.imwrite("intruder.jpg", frame)
                send_image_email(
                    subject="Pythony Security Alert",
                    image_filename="intruder.jpg",
                    body="an Unauthorized User has started your computer",
                    reciever_email=os.getenv("PROFESSIONAL_EMAIL"),
                )
                break
        cv2.imshow("Security Camera", frame)
        # if you press q close the window
        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("Camera shut off")
            break
    print("program ended")
    cap.release()
    cv2.destroyAllWindows()
