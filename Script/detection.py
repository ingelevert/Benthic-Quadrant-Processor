import cv2
import numpy as np

class QuadrantDetector:
    def detect_automatically(self, image):
        # Simplified detection because complex drops too many images
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        best_corners = None
        best_score = 0
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 10000:
                continue
            
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            if len(approx) == 4:
                corners = approx.reshape(4, 2)
                score = self._calculate_score(corners, area)
                if score > best_score:
                    best_score = score
                    best_corners = corners
        
        return self._sort_corners(best_corners) if best_corners is not None else None
    
    def detect_with_fallback(self, image, ui):
        corners = self.detect_automatically(image)
        if corners is not None:
            print("✓ Auto-detected quadrant")
            return corners
        else:
            print("⚠ Auto-detection failed, switching to manual")
            return ui.manual_corner_selection(image)
    
    def _calculate_score(self, corners, area):
        # Simplified scoring
        sides = [np.linalg.norm(corners[i] - corners[(i+1)%4]) for i in range(4)]
        if np.mean(sides) == 0:
            return 0
        return 1.0 / (1.0 + np.std(sides) / np.mean(sides)) * min(area / 50000, 1.0)
    
    def _sort_corners(self, corners):
        # Sort corners properly, had issues sorting
        if corners is None:
            return None
        centroid = np.mean(corners, axis=0)
        angles = [np.arctan2(p[1] - centroid[1], p[0] - centroid[0]) for p in corners]
        sorted_corners = [corners[i] for i in np.argsort(angles)]
        sums = [p[0] + p[1] for p in sorted_corners]
        tl_idx = np.argmin(sums)
        return np.roll(sorted_corners, -tl_idx, axis=0)