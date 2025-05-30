from quadrant_processor import GoProQuadrantProcessor
import os

def main():
    processor = GoProQuadrantProcessor()
    
    # Load the calibration
    if not processor.load_calibration():
        print("\nNo camera calibration found.")
        response = input("Do you want to calibrate now? (y/n): ").lower()
        if response == 'y':
            calib_path = input("Enter calibration images folder path: ").strip().strip('"')
            if not processor.calibrate_camera(calib_path):
                print("\n⚠ Calibration failed. Proceeding without distortion correction.")
    
    # Processing menu ui
    print("\n" + "="*50)
    print("BENTHIC QUADRANT PROCESSOR BY LEVI LINA")
    print("="*50)
    print("1. Process only a single image")
    print("2. Batch process folder of pictures")
    
    choice = input("\nChoose processing mode (1 or 2): ").strip()
    
    if choice == "1":
        processor.single_image_mode()
    elif choice == "2":
        processor.batch_mode()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()