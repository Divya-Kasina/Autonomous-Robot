# save_calibration_images.py
import cv2
import os

cap = cv2.VideoCapture(0)
i = 0
save_dir = "calib_images"
os.makedirs(save_dir, exist_ok=True)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow("Press SPACE to save, ESC to exit", frame)
    key = cv2.waitKey(1)
    if key == 27:  # ESC
        break
    elif key == 32:  # SPACE
        filename = os.path.join(save_dir, f"img_{i:02d}.jpg")
        cv2.imwrite(filename, frame)
        print(f"Saved {filename}")
        i += 1

cap.release()
cv2.destroyAllWindows()
