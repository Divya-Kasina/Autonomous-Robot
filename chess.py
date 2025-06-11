import cv2
import numpy as np

# Load camera calibration
data = np.load("calibration_data.npz")
camera_matrix = data["camera_matrix"]
dist_coeffs = data["dist_coeffs"]

CHECKERBOARD = (9, 6)
objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret_corners, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

    if ret_corners:
        cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1),
                         (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
        
        # Pose estimation
        ret, rvec, tvec = cv2.solvePnP(objp, corners, camera_matrix, dist_coeffs)

        # Draw axis
        cv2.drawFrameAxes(frame, camera_matrix, dist_coeffs, rvec, tvec, 3)

        cv2.putText(frame, f"X: {tvec[0][0]:.2f} Y: {tvec[1][0]:.2f} Z: {tvec[2][0]:.2f}",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)

    cv2.imshow("Pose Estimation", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
