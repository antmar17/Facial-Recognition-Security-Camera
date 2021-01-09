import cv2
import numpy as np


def detect_faces(original_img):

    # DNN model files
    modelFile = "Model_files\\res10_300x300_ssd_iter_140000_fp16.caffemodel"
    configFile = "Model_Files\\deploy.prototxt"
    net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
    h, w = original_img.shape[:2]
    blob = cv2.dnn.blobFromImage(
        cv2.resize(original_img, (300, 300)), 1.0, (300, 300), (104.0, 117.0, 123.0)
    )

    net.setInput(blob)
    faces = net.forward()
    print(faces)

    for i in range(faces.shape[2]):
        confidence = faces[0, 0, i, 2]

        # if the program is confident enough that it is a face then draw a box around it!
        if confidence > 0.5:
            box = faces[0, 0, i, 3:7] * np.array([w, h, w, h])
            text = "{:.2f}%".format(confidence * 100)
            (startX, startY, endX, endY) = box.astype("int")
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.rectangle(original_img, (startX, startY), (endX, endY), (255, 0, 0), 2)
            cv2.putText(
                original_img,
                text,
                (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (255, 0, 0),
                2,
            )


if __name__ == "__main__":

    # capture video
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        ret, frame = cap.read()
        print(type(frame))

        detect_faces(frame)
        cv2.imshow("my face", frame)

        # if you press q close the window
        if cv2.waitKey(1) % 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()
