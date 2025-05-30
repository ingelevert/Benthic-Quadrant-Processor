# Benthic Quadrant Corrector

A image processing tool designed for correcting and enhancing benthic quadrant images captured with GoPro cameras underwater. This tool performs lens distortion correction, perspective correction, and color enhancement specifically optimized for marine research applications.

## 🌊 What it does

This tool processes underwater GoPro images of benthic quadrants by:

- **Camera Calibration**: Corrects lens distortion using chessboard calibration images
- **Quadrant Detection**: Automatically detects quadrant corners or allows manual selection
- **Perspective Correction**: Transforms angled quadrant views into perfect top-down squares (2000x2000 pixels)
- **Chromatic Aberration Correction**: Aligns color channels (to green) to reduce underwater optical artifacts
- **Color Enhancement**: Restores red tones lost in underwater photography
- **Batch Processing**: Processes multiple images efficiently with consistent settings

## 🔬 Perfect for Marine Research

Designed specifically for:
- Benthic habitat monitoring
- Species identification and counting
- Coral reef surveys
- Marine biodiversity assessments
- Standardized quadrat sampling

## Features

- **High-Quality Output**: 2000x2000 pixel (4MP) corrected images at 98% JPEG quality
- **Color Restoration**: Specialized underwater color correction algorithms
- **Batch Processing**: Process entire folders of images with progress tracking
- **Interactive UI**: Click-based corner selection with visual feedback
- **Calibration Support**: Built-in camera calibration for optimal distortion correction

## 📋 Requirements

```txt
opencv-python
numpy
```

## 🛠️ Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/Benthic_Quadrant_Corrector.git
cd Benthic_Quadrant_Corrector
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
cd FINAL
python main.py
```

## 📖 Usage

### First Time Setup - Camera Calibration

1. **Prepare calibration images**: Take 20-40 photos of a chessboard pattern with your GoPro underwater (if possible) or in similar conditions
2. **Run calibration**: The tool will prompt you to calibrate if no calibration file is found
3. **Enter parameters**: 
   - Internal corners width (default: 8)
   - Internal corners height (default: 6) 
   - Square size in cm (default: 3.025)

### Processing Images

The tool offers two modes:

#### Single Image Mode
- Process one image at a time
- Perfect for testing or individual image correction
- Interactive corner selection if auto-detection fails

#### Batch Processing Mode
- Process entire folders of images
- Consistent color enhancement settings across all images
- Progress tracking and error handling
- Skip problematic images while continuing the batch

### Controls During Processing

- **Left Click**: Select quadrant corners (Top-Left → Top-Right → Bottom-Right → Bottom-Left)
- **Right Click**: Reset corner selection
- **SPACE**: Process current image (when 4 corners selected)
- **N**: Skip current image
- **ESC**: Cancel processing


## Output

Each processed image produces:
- **Resolution**: 2000x2000 pixels (perfect square)
- **Quality**: 98% JPEG compression
- **Naming**: `[original_name]_Corrected.jpg`
- **Color Space**: Enhanced BGR with restored red channel
- **Geometric**: Corrected perspective and lens distortion


### Perspective Correction
- 4-point perspective transformation
- Maps quadrant corners to perfect square coordinates
- Maintains aspect ratio and content integrity

### Color Enhancement
- **Chromatic Aberration Correction**: Aligns RGB channels with sub-pixel precision
- **Red Channel Boost**: Compensates for red light absorption underwater
- **Saturation Enhancement**: Restores color vibrancy lost in aquatic environments

## 🤝 Contributing

This tool was developed for marine research applications. Contributions are welcome, especially:
- Additional color correction algorithms
- Support for other camera types
- Automated quadrant size detection
- Integration with marine analysis software

## 📝 License

MIT License

## 👨‍💻 Author

Created by Levi Lina for benthic marine research applications.

## 🙏 Acknowledgments

- OpenCV community for computer vision tools
- Marine research community for testing and feedback
- Wageningen University & Research for calibration standards and the opportunity to build this application

---

*Perfect for marine biologists, underwater photographers, and research institutions working with benthic quadrat sampling.*
