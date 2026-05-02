import face_recognition
import cv2
import pickle
import numpy as np

# Load encodings
with open("encodings.pkl", "rb") as f:
    data = pickle.load(f)

print("👤 Loaded students:", set(data["names"]))

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

        matches = face_recognition.compare_faces(data["encodings"], face_encoding)
        face_distances = face_recognition.face_distance(data["encodings"], face_encoding)

        name = "Unknown"

        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)

            # 🔥 STRICT THRESHOLD (VERY IMPORTANT)
            if face_distances[best_match_index] < 0.5:
                name = data["names"][best_match_index]

        # Scale back coordinates
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2

        # Draw box + name
        cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
        cv2.putText(frame, name, (left, top-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()