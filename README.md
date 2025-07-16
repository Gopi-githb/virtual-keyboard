Introduction

Virtual Keyboard using Hand Tracking

This project implements a gesture-based virtual keyboard using Python, OpenCV, and the CVZone library. The system leverages real-time hand detection to allow users to type without physical contact—ideal for accessibility tools, hygienic public interfaces, and experimental input systems.


Features

--Real-time hand and fingertip tracking (via CVZone & MediaPipe)
--On-screen QWERTY keyboard with support for:
    1.Shift (uppercase toggle)
    2.Spacebar
    3.Backspace
--Touchless "tap" detection using downward movement of the index finger
--Live display of typed text in a formatted container
--Debounce logic to avoid multiple key entries per tap



Technologies Used

--Python 3
--OpenCV – For image processing and UI rendering
--CVZone – Simplifies hand detection using MediaPipe
--MediaPipe – Underlying hand tracking model
--NumPy, Time – For data handling and timing control

How It Works
1.The webcam captures live video.
2.The HandTrackingModule detects the hand and tracks the index finger.
3.A virtual keyboard is drawn on the screen.
4.When the index finger "taps" a virtual key (detected by movement), the corresponding character is added to the output.
5.The typed text is shown in a styled output container.


Demo
(You can upload a demo gif or short video here)


Use Cases
--Touchless typing interfaces
--Virtual reality or augmented reality input methods
--Accessible input for users with motor impairments
--Smart kiosks or public systems requiring contact-free interaction


Setup Instructions

1.Install dependencies:
     bash
     pip install opencv-python cvzone

2.Run the script:
     bash
     python virtual_keyboard.py

3.Ensure your webcam is connected and allow camera permissions if prompted.

