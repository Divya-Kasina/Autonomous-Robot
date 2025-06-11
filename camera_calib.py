import cv2
import numpy as np
import os

# Chessboard dimensions
CHECKERBOARD = (9, 6)

# Criteria for corner refinement
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

objpoints = []  # 3d points in real world
imgpoints = []  # 2d points in image plane

cap = cv2.VideoCapture(0)

count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret_corners, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

    if ret_corners:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners2)
        cv2.drawChessboardCorners(frame, CHECKERBOARD, corners2, ret_corners)
        count += 1
        print(f"Captured image {count}")

    cv2.imshow('Calibration', frame)
    if cv2.waitKey(1) & 0xFF == ord('q') or count >= 15:
        break

cap.release()
cv2.destroyAllWindows()

ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
    objpoints, imgpoints, gray.shape[::-1], None, None
)

print("\nCamera matrix:\n", camera_matrix)
print("Distortion coefficients:\n", dist_coeffs)

# Save calibration
np.savez("calibration_data.npz", camera_matrix=camera_matrix, dist_coeffs=dist_coeffs)
