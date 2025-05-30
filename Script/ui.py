import cv2
import numpy as np

#the ui
class UserInterface:
    def __init__(self):
        self.corners = []
        self.image = None
        self.original_image = None
    
    def get_red_level(self):
        while True:
            try:
                level = int(input("Enter red enhancement level (1-5): "))
                if 1 <= level <= 5:
                    return level
                print("Please enter 1-5")
            except ValueError:
                print("Please enter a number")
    
    def manual_corner_selection(self, image):
        self.original_image = image.copy()
        self.image = image.copy()
        self.corners = []
        
        self._add_grid()
        self._add_instructions()
        
        cv2.imshow('Manual Corner Selection', self.image)
        cv2.setMouseCallback('Manual Corner Selection', self._mouse_callback)
        
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                cv2.destroyAllWindows()
                return "cancel"
            elif key == ord('n') or key == ord('N'):  # N - skip
                cv2.destroyAllWindows()
                return "skip"
            elif key == 32 and len(self.corners) == 4:  # SPACE
                cv2.destroyAllWindows()
                return np.array(self.corners, dtype=np.float32)
    
    def _mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN and len(self.corners) < 4:
            self.corners.append([x, y])
            self._redraw()
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.corners = []
            self._redraw()
    
    def _redraw(self):
        if self.original_image is None:
            return
        self.image = self.original_image.copy()
        self._add_grid()
        self._add_instructions()
        
        # Draw corners
        labels = ["TL", "TR", "BR", "BL"]
        for i, corner in enumerate(self.corners):
            cv2.circle(self.image, tuple(corner), 10, (0, 255, 0), -1)
            cv2.putText(self.image, labels[i], (corner[0]+15, corner[1]-15),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            if i > 0:
                cv2.line(self.image, tuple(self.corners[i-1]), tuple(corner), (0, 255, 0), 2)
        
        if len(self.corners) == 4:
            cv2.line(self.image, tuple(self.corners[-1]), tuple(self.corners[0]), (0, 255, 0), 2)
            cv2.putText(self.image, "SPACE to continue, N to skip", 
                       (10, self.image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        cv2.imshow('Manual Corner Selection', self.image)
    
    def _add_grid(self):
        if self.image is None:
            return
        h, w = self.image.shape[:2]
        spacing = max(min(w, h) // 20, 1)
        for i in range(0, w, spacing):
            cv2.line(self.image, (i, 0), (i, h), (200, 200, 200), 1)
        for i in range(0, h, spacing):
            cv2.line(self.image, (0, i), (w, i), (200, 200, 200), 1)
    
    def _add_instructions(self):
        if self.image is None:
            return
        instructions = [
            "Click corners: TL -> TR -> BR -> BL",
            f"Right-click reset, SPACE when done ({len(self.corners)}/4), N to skip"
        ]
        for i, text in enumerate(instructions):
            cv2.putText(self.image, text, (10, 30 + i*25), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)