import cv2
import numpy as np
import os
from calibration import CameraCalibrator
from detection import QuadrantDetector
from processing import ImageProcessor
from ui import UserInterface

class GoProQuadrantProcessor:
    def __init__(self, quadrant_size_cm=50):
        self.quadrant_size_cm = quadrant_size_cm
        self.calibrator = CameraCalibrator()
        self.detector = QuadrantDetector()
        self.processor = ImageProcessor()
        self.ui = UserInterface()
        
    def load_calibration(self):
        return self.calibrator.load_calibration()
    
    def calibrate_camera(self, path):
        return self.calibrator.calibrate_camera(path)
    
    def single_image_mode(self):
        while True:
            image_path = input("\nEnter image path (or 'q' to quit): ").strip().strip('"')
            if image_path.lower() == 'q':
                break
                
            if not os.path.exists(image_path):
                print(f"❌ Image not found")
                continue
            
            red_level = self.ui.get_red_level()
            result = self.process_single_image(image_path, red_level)
            
            if result:
                another = input("\nProcess another? (y/n): ").lower()
                if another != 'y':
                    break
    
    def batch_mode(self):
        print("\n" + "="*50)
        print("BATCH PROCESSING SETUP")
        print("="*50)
        
        # Get input folder
        while True:
            input_folder = input("\nEnter path to folder containing images: ").strip().strip('"')
            if os.path.exists(input_folder):
                # Count images in folder
                image_files = []
                for ext in ['*.jpg', '*.jpeg', '*.JPG', '*.JPEG', '*.png', '*.PNG']:
                    import glob
                    image_files.extend(glob.glob(os.path.join(input_folder, ext)))
                
                if image_files:
                    print(f"✅ Found {len(image_files)} images in input folder")
                    break
                else:
                    print("❌ No images found in this folder")
            else:
                print("❌ Folder not found, please try again")
        
        # Get output folder
        while True:
            output_folder = input("\nEnter path for output folder (will be created if it doesn't exist): ").strip().strip('"')
            
            if output_folder:
                # Try to create the folder 
                try:
                    os.makedirs(output_folder, exist_ok=True)
                    print(f"✅ Output folder ready: {output_folder}")
                    break
                except Exception as e:
                    print(f"❌ Cannot create output folder: {e}")
                    print("Please enter a valid path")
            else:
                print("❌ Please enter a folder path")
        
        # Get red levels
        print("\nColor Enhancement Settings:")
        red_level = self.ui.get_red_level()
        
        # Confirm
        print(f"\n" + "="*50)
        print("BATCH PROCESSING SUMMARY")
        print("="*50)
        print(f"📁 Input folder:  {input_folder}")
        print(f"📤 Output folder: {output_folder}")
        print(f"🎨 Red level:     {red_level}/5")
        print(f"📸 Images found:  {len(image_files)}")
        print("\n💡 During processing:")
        print("   • SPACE = Process current image")
        print("   • N = Skip current image") 
        print("   • ESC = Cancel entire batch")
        
        confirm = input(f"\nProceed with batch processing? (y/n): ").lower()
        if confirm != 'y':
            print("Batch processing cancelled.")
            return
        
        # Start 
        self.processor.batch_process_manual(input_folder, output_folder, red_level, 
                                          self.calibrator, self.detector, self.ui)
    
    def process_single_image(self, image_path, red_level):
        # Load and undistort
        image = cv2.imread(image_path)
        if image is None:
            return False
            
        print(f"✅ Image loaded: {image.shape[1]}x{image.shape[0]} pixels")
        undistorted = self.calibrator.undistort_image(image)
        print("✅ Lens distortion corrected")
        
        # Detect or manually select corners
        corners = self.detector.detect_with_fallback(undistorted, self.ui)
        if corners is None or isinstance(corners, str):
            return False
        
        print("✅ Corners selected")
        
        # Process and save
        print("🔧 Correcting perspective to 2000x2000...")
        corrected = self.processor.correct_perspective(undistorted, corners, output_size=2000)
        print("🌈 Enhancing colors and correcting chromatic aberration...")
        enhanced = self.processor.enhance_colors(corrected, red_level)
        
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        output_path = f"{base_name}_Corrected.jpg"
        
        # Save with high quality
        cv2.imwrite(output_path, enhanced, [cv2.IMWRITE_JPEG_QUALITY, 95])
        
        print(f"✅ Saved: {output_path} (2000x2000, 95% quality)")
        return True