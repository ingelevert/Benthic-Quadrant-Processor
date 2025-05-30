import cv2
import numpy as np
import pickle
import glob
import os

class CameraCalibrator:
    def __init__(self):
        self.camera_matrix = None
        self.dist_coeffs = None
    
    def calibrate_camera(self, calibration_folder):
        # simple calibration
        if not os.path.exists(calibration_folder):
            return False
        
        # Get user parameters, the default ones are the ones that the WUR uses with the quadrants
        width = int(input("Internal corners width (default 8): ") or "8")
        height = int(input("Internal corners height (default 6): ") or "6")
        square_size = float(input("Square size in cm (default 3.025): ") or "3.025")
        
        chessboard_size = (width, height)
        
        # Find images
        image_files = []
        for ext in ['*.jpg', '*.jpeg', '*.JPG', '*.JPEG', '*.png', '*.PNG']:
            image_files.extend(glob.glob(os.path.join(calibration_folder, ext)))
        
        if not image_files:
            print("No images found")
            return False
        
        # Calibration logics
        objp = np.zeros((width * height, 3), np.float32)
        objp[:,:2] = np.mgrid[0:width, 0:height].T.reshape(-1,2) * square_size
        
        objpoints = []
        imgpoints = []
        image_size = None
        
        for fname in image_files:
            img = cv2.imread(fname)
            if img is None:
                continue
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            if image_size is None:
                image_size = gray.shape[::-1]
            ret, corners = cv2.findChessboardCorners(gray, chessboard_size)
            
            if ret:
                objpoints.append(objp)
                corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), 
                    (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
                imgpoints.append(corners2)
                print(f"✓ {os.path.basename(fname)}")
        if len(objpoints) < 3:
            print("Need at least 3 good images")
            return False
        
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
            objpoints, imgpoints, image_size, None, None, None, None, cv2.CALIB_FIX_ASPECT_RATIO) # type: ignore
        
        self.camera_matrix = mtx
        self.dist_coeffs = dist
        
        # Save the calibration
        with open('gopro_calibration.pkl', 'wb') as f:
            pickle.dump({'camera_matrix': mtx, 'distortion_coefficients': dist}, f)
        
        print(f"✅ Calibration complete! RMS Error: {ret:.3f}")
        return True
    
    def load_calibration(self):
        try:
            with open('gopro_calibration.pkl', 'rb') as f:
                data = pickle.load(f)
            self.camera_matrix = data['camera_matrix']
            self.dist_coeffs = data['distortion_coefficients']
            print("✓ Calibration loaded")
            return True
        except:
            return False
    
    def undistort_image(self, image):
        if self.camera_matrix is None or self.dist_coeffs is None:
            return image
        
        h, w = image.shape[:2]
        new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(
            self.camera_matrix, self.dist_coeffs, (w, h), alpha=1)
        return cv2.undistort(image, self.camera_matrix, self.dist_coeffs, None, new_camera_matrix)