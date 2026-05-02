import face_recognition
import os
import pickle
import cv2

dataset_path = "dataset"

known_encodings = []
known_names = []

# 🔥 Delete old encoding file (important)
if os.path.exists("encodings.pkl"):
    os.remove("encodings.pkl")
    print("🗑 Old encodings deleted")

print("⏳ Encoding started...")

for person_name in os.listdir(dataset_path):
    person_folder = os.path.join(dataset_path, person_name)

    for image_name in os.listdir(person_folder):
        image_path = os.path.join(person_folder, image_name)

        image = face_recognition.load_image_file(image_path)

        # 🔥 Resize for speed
        image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)

        encodings = face_recognition.face_encodings(image)

        if len(encodings) > 0:
            known_encodings.append(encodings[0])
            known_names.append(person_name)

print("💾 Saving encodings...")

data = {"encodings": known_encodings, "names": known_names}

with open("encodings.pkl", "wb") as f:
    pickle.dump(data, f)

print("✅ Encoding completed!")
print("👤 Students in system:", set(known_names))