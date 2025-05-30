import cv2
import numpy as np
import glob
import os

class ImageProcessor:
    def correct_perspective(self, image, corners, output_size=2000):  # Increased from 1000 to 2000
        dst_corners = np.array([[0, 0], [output_size-1, 0], 
                               [output_size-1, output_size-1], [0, output_size-1]], dtype=np.float32)
        M = cv2.getPerspectiveTransform(corners.astype(np.float32), dst_corners)
        return cv2.warpPerspective(image, M, (output_size, output_size))
    
    def correct_chromatic_aberration(self, image):
        """Correct chromatic aberration by aligning color channels"""
        # Split into BGR channels for chromatic abberation
        b, g, r = cv2.split(image)
        
        # Use green channel as reference since blue and red change underwater
        h, w = g.shape
        
        # Calculate shifts for red and blue channels
        # These values work well for most GoPro images, but can be fine-tuned
        red_shift_x, red_shift_y = 1.5, 1.0      # Red channel shift
        blue_shift_x, blue_shift_y = -1.0, -0.5  # Blue channel shift
        
        # Create transformation matrices
        M_red = np.array([[1, 0, red_shift_x], [0, 1, red_shift_y]], dtype=np.float32)
        M_blue = np.array([[1, 0, blue_shift_x], [0, 1, blue_shift_y]], dtype=np.float32)
        
        # Apply shifts
        r_corrected = cv2.warpAffine(r, M_red, (w, h), flags=cv2.INTER_LINEAR)
        b_corrected = cv2.warpAffine(b, M_blue, (w, h), flags=cv2.INTER_LINEAR)
        
        # Merge channels back
        corrected = cv2.merge([b_corrected, g, r_corrected])
        
        return corrected
    
    def enhance_colors(self, image, red_level=5):
        # First correct chromatic aberration
        image = self.correct_chromatic_aberration(image)
        
        red_boost = 1.0 + (red_level - 1) * 0.125
        saturation_boost = 1.0 + (red_level - 1) * 0.05
        
        img_float = image.astype(np.float32) / 255.0
        img_float[:, :, 2] = np.clip(img_float[:, :, 2] * red_boost, 0, 1)
        
        hsv = cv2.cvtColor(img_float, cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * saturation_boost, 0, 1)
        
        enhanced = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return (enhanced * 255).astype(np.uint8)
    
    def batch_process_manual(self, input_folder, output_folder, red_level, calibrator, detector, ui):
        # Find images
        image_files = []
        for ext in ['*.jpg', '*.jpeg', '*.JPG', '*.JPEG', '*.png', '*.PNG']:
            image_files.extend(glob.glob(os.path.join(input_folder, ext)))
        
        print(f"\n🚀 Starting batch processing...")
        print(f"📐 Output resolution: 2000x2000 pixels (4MP)")
        print(f"🌈 Chromatic aberration correction: ENABLED")
        
        successful = 0
        skipped = 0
        failed = 0
        
        for i, image_path in enumerate(image_files, 1):
            print(f"\n{'='*60}")
            print(f"IMAGE {i} of {len(image_files)}: {os.path.basename(image_path)}")
            print(f"{'='*60}")
            
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                print("❌ Failed to load image")
                failed += 1
                continue
            
            print(f"✅ Image loaded: {image.shape[1]}x{image.shape[0]} pixels")
            
            # Undistort
            undistorted = calibrator.undistort_image(image)
            print("✅ Lens distortion corrected")
            
            # Manual corner selection
            print("🖱 Please select corners in the image window...")
            corners = ui.manual_corner_selection(undistorted)
            
            # Check if corners is a string (cancel/skip) or None/array
            if isinstance(corners, str):
                if corners == "cancel":
                    print("\n🛑 Batch processing cancelled by user")
                    break
                elif corners == "skip":
                    print("⏭ Image skipped")
                    skipped += 1
                    continue
                else:
                    print("❌ Corner selection failed")
                    failed += 1
                    continue
            elif corners is None:
                print("❌ Corner selection failed")
                failed += 1
                continue
            
            print("✅ Corners selected")
            
            # Process image
            print("🔧 Correcting perspective...")
            corrected = self.correct_perspective(undistorted, corners, output_size=2000)
            print(f"✅ Perspective corrected to 2000x2000 pixels")
            
            print("🌈 Enhancing colors and correcting chromatic aberration...")
            enhanced = self.enhance_colors(corrected, red_level)
            print("✅ Color enhancement complete")
            
            # Save with higher quality
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            output_path = os.path.join(output_folder, f"{base_name}_Corrected.jpg")
            
            # Save with high quality, i chose 98%, because of species identification
            cv2.imwrite(output_path, enhanced, [cv2.IMWRITE_JPEG_QUALITY, 98])
            
            successful += 1
            print(f"✅ Saved: {base_name}_Corrected.jpg (2000x2000, 95% quality)")
        
        # Final summary for the user
        print(f"\n" + "="*60)
        print("BATCH PROCESSING COMPLETE")
        print("="*60)
        print(f"✅ Successfully processed: {successful}")
        print(f"⏭ Skipped: {skipped}")
        print(f"❌ Failed: {failed}")
        print(f"📁 Results saved in: {output_folder}")
        print(f"📐 Output: 2000x2000 pixels (4MP) per image")
        print(f"🌈 Chromatic aberration corrected")