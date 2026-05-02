import cv2
import os

DATASET_PATH = "dataset"

# Load face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def is_processed(img):
    # Check if already grayscale and resized
    if len(img.shape) == 2 and img.shape == (160, 160):
        return True
    return False

def process_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return None

    (x, y, w, h) = faces[0]
    face = gray[y:y+h, x:x+w]

    face = cv2.resize(face, (160, 160))
    face = cv2.equalizeHist(face)
    face = cv2.GaussianBlur(face, (3, 3), 0)

    return face


for student in os.listdir(DATASET_PATH):
    student_path = os.path.join(DATASET_PATH, student)

    if not os.path.isdir(student_path):
        continue

    for img_name in os.listdir(student_path):
        img_path = os.path.join(student_path, img_name)

        # Skip already processed files
        if "_clean" in img_name:
            continue

        img = cv2.imread(img_path)
        if img is None:
            continue

        if is_processed(img):
            print(f"⏩ Skipped (already clean): {img_name}")
            continue

        processed = process_image(img)

        if processed is not None:
            # Save with _clean suffix
            new_name = img_name.split(".")[0] + "_clean.jpg"
            save_path = os.path.join(student_path, new_name)

            cv2.imwrite(save_path, processed)
            print(f"✅ Processed: {new_name}")

        else:
            print(f"❌ No face detected: {img_name}")

print("🎯 Only new images processed successfully!")