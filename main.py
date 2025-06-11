import cv2
import numpy as np
import socket
import json

# Load camera calibration
calib_data = np.load("calibration_data.npz")
camera_matrix = calib_data["camera_matrix"]
dist_coeffs = calib_data["dist_coeffs"]

# Chessboard dimensions
CHECKERBOARD = (9, 6)
square_size = 0.024  # meters

# 3D object points
objp = np.zeros((CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
objp *= square_size

# UDP setup
UDP_IP = "172.25.127.86"  # WSL or Ubuntu IP (you can also try "localhost" or check with `ip addr` in Ubuntu)
UDP_PORT = 9999
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cap = cv2.VideoCapture(0)
print("Camera opened:", cap.isOpened())

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    found, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

    if found:
        corners_refined = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1),
                                           (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
        success, rvec, tvec = cv2.solvePnP(objp, corners_refined, camera_matrix, dist_coeffs)

        if success:
            # Draw 3D axes
            cv2.drawFrameAxes(frame, camera_matrix, dist_coeffs, rvec, tvec, 0.1)

            # Prepare and send JSON data
            data = {
                "rvec": rvec.flatten().tolist(),
                "tvec": tvec.flatten().tolist()
            }
            sock.sendto(json.dumps(data).encode(), (UDP_IP, UDP_PORT))
            print("Sent data to {}:{} -> {}".format(UDP_IP, UDP_PORT, data))


        cv2.drawChessboardCorners(frame, CHECKERBOARD, corners_refined, found)

    cv2.imshow("Pose Estimation", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
