# AI-Based Anxiety-Related Visual Signal Monitoring Using Computer Vision

A computer vision web application developed as an academic project to explore real-time facial detection and visual signal monitoring using a webcam.

**Author:** Komal Rafique  
**Field:** Computer Science, Artificial Intelligence and Computer Vision  
**Project Status:** Academic prototype

## Overview

This project combines Python, OpenCV, and Flask to create a webcam-based interface that detects faces and displays an experimental visual-signal score in real time.

The current implementation uses Haar Cascade classifiers for face and smile detection. A rule-based heuristic calculates a score from changes in detected face area, smile detection, and missing-face frames.

**Important:** The score is an experimental software output. It is not a clinically validated anxiety measurement and must not be used for medical diagnosis.

## Features

- Real-time webcam feed
- Face detection using OpenCV Haar Cascades
- Smile detection using OpenCV
- Rule-based experimental score calculation
- Live score display and LOW, MODERATE, and HIGH labels
- Live chart using Chart.js
- Flask-based web dashboard
- Basic session-based username interface
- Experimental sound alert
- Text report and history-related project components

## Technology Stack

- Python
- Flask
- OpenCV
- HTML5 and CSS3
- JavaScript
- Chart.js
- SQLite

## Project Structure

```text
Anxiety_Detection_Project/
├── app.py
├── requirements.txt
├── database.db
├── haarcascade_frontalface_default.xml
├── anxiety_report.txt
├── reports/
├── static/
└── templates/
    ├── history.html
    ├── index.html
    └── login.html
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/komalcoder357/AI-Based-Anxiety-Detection-System-Using-Computer-Vision.git
```

### 2. Open the project directory

```bash
cd AI-Based-Anxiety-Detection-System-Using-Computer-Vision/Anxiety_Detection_Project
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python app.py
```

Open `http://127.0.0.1:5000` in your browser and allow webcam access if prompted.

The application requires a working webcam. Camera availability and browser permissions may affect operation.

## Current Methodology

1. Capture frames from the webcam using OpenCV.
2. Convert frames to grayscale.
3. Detect faces using a Haar Cascade classifier.
4. Apply smile detection within detected face regions.
5. Calculate an experimental score using manually defined rules.
6. Display the score and category in the web interface.

The current `app.py` does not load a trained anxiety-classification model. Its score is rule-based rather than a learned prediction.

## Limitations

- The score has not been clinically validated.
- Facial movement and smiling do not reliably establish a person's emotional state or anxiety.
- The current implementation does not demonstrate a trained anxiety-classification model.
- No verified model accuracy or clinical evaluation results are claimed.
- The current login interface is not a complete authentication system.

## Future Improvements

- Evaluate a clearly defined computer vision task using an appropriate labeled dataset.
- Separate face detection from any emotion-related classification model.
- Add reproducible evaluation metrics and documented experimental results.
- Improve camera lifecycle management and application security.
- Add screenshots, testing instructions, and reproducible setup documentation.
- Explore privacy-conscious webcam processing.

## Ethical Considerations

This project is intended for educational and research exploration. It does not diagnose anxiety, replace professional assessment, or establish a person's mental health from facial appearance. Webcam data should be handled with informed consent and appropriate privacy safeguards.

## License

No license has been specified yet. Contact the repository owner before reusing or redistributing this project.
