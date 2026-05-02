import face_recognition
import cv2
import numpy as np
import dlib
from imutils import face_utils
import pickle

# Load encodings
with open("encodings.pkl", "rb") as f:
    data = pickle.load(f)

print("👤 Loaded students:", set(data["names"]))

# Load dlib
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

def eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    return (A + B) / (2.0 * C)

def recognize_face(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 🔥 Blink detection
    rects = detector(gray, 0)
    blink_detected = False

    for rect in rects:
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]

        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        ear = (leftEAR + rightEAR) / 2.0

        if ear < 0.25:
            blink_detected = True

    # 🔥 Face recognition
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    results = []

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

        face_distances = face_recognition.face_distance(data["encodings"], face_encoding)

        name = "Unknown"

        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)

            if face_distances[best_match_index] < 0.5 and blink_detected:
                name = data["names"][best_match_index]
            elif face_distances[best_match_index] < 0.5:
                name = "Fake/No Blink"

        # scale back
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2

        results.append((top, right, bottom, left, name))

    return results


# 🔥 TEST MODE (run this file directly)
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = recognize_face(frame)

        for (top, right, bottom, left, name) in results:
            cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
            cv2.putText(frame, name, (left, top-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

        cv2.imshow("Test Camera", frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()