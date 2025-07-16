import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep

# Initialize Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Camera Setup
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Keyboard Layout
keys = [
    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", "@"],
    ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
    ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")"],
    ["<-", "Shift", "Spc"]  # Shift and Spacebar
]

finalText = ""
prev_tap = False
shift_mode = False  # Track Shift Mode
prev_y = None  # Previous Y-position of index finger

# Button Class
class Button:
    def __init__(self, pos, text, size=[60, 50]):
        self.pos = pos
        self.size = size
        self.text = text

# Create Button List
buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        if key == "Spc":
            buttonList.append(Button([250, 550], "Space", [300, 50]))  # Spacebar
        elif key == "Shift":
            buttonList.append(Button([50, 550], "Shift", [100, 50]))  # Shift Key
        elif key == "<-":
            buttonList.append(Button([600, 550], "<-", [100, 50]))  # Backspace
        else:
            buttonList.append(Button([70 * j + 50, 70 * i + 200], key, [60, 50]))

# Function to Draw Keyboard
def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, (x, y), (x + w, y + h), (50, 50, 150), cv2.FILLED)
        cv2.putText(img, button.text, (x + 10, y + 35), 
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
    return img

# Format Output Text
def formatText(text, max_length=25):
    words = text.split(" ")
    lines, line = [], ""
    for word in words:
        if len(line) + len(word) < max_length:
            line += word + " "
        else:
            lines.append(line.strip())
            line = word + " "
    lines.append(line.strip())
    return lines

# Main Loop
while True:
    success, img = cap.read()
    if not success:
        continue
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, draw=False)
    img = drawAll(img, buttonList)

    if hands:
        lmList = hands[0]['lmList']
        x1, y1 = lmList[8][:2]  # Index Finger Tip

        if prev_y is None:
            prev_y = y1  # Initialize previous Y-position

        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            # Check if the index finger is inside a button
            if x < x1 < x + w and y < y1 < y + h:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, button.text, (x + 10, y + 35),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

                # Check downward movement (tap) before registering input
                if y1 > prev_y + 10 and not prev_tap:  # Detect downward movement (tap)
                    if button.text == "<-":
                        finalText = finalText[:-1]  # Remove Last Character
                    elif button.text == "Shift":
                        shift_mode = not shift_mode  # Toggle Shift Mode
                    elif button.text == "Space":
                        finalText += " "  # Add Space
                    else:
                        finalText += button.text.upper() if shift_mode else button.text.lower()
                    
                    prev_tap = True  # Mark that a tap occurred
                    sleep(0.15)
                
                # Reset tap when finger is lifted
                elif y1 < prev_y - 10:
                    prev_tap = False

        prev_y = y1  # Update previous Y-position

    # Draw Text Output Container
    cv2.rectangle(img, (50, 40), (900, 150), (50, 50, 150), cv2.FILLED)
    lines = formatText(finalText)
    y_offset = 80
    for line in lines:
        cv2.putText(img, line, (60, y_offset),
                    cv2.FONT_HERSHEY_COMPLEX, 1.5, (255, 255, 255), 3)
        y_offset += 40

    cv2.imshow("Virtual Keyboard", img)
    cv2.waitKey(1)
