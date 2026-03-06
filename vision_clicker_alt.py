import pyautogui
import cv2
import numpy as np
import easyocr
import time

# Initialize OCR reader once
print("Initializing OCR engine...")
reader = easyocr.Reader(['en'], gpu=False)


def find_and_click(target):

    target = target.lower()

    print(f"\nSearching for text: '{target}'")

    # Try multiple times (screen may update slowly)
    for attempt in range(5):

        print(f"Vision attempt {attempt+1}...")

        # Take screenshot
        screenshot = pyautogui.screenshot()

        img = np.array(screenshot)

        # Convert RGB → BGR for OpenCV
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # Run OCR
        results = reader.readtext(img_bgr)

        for (bbox, text, confidence) in results:

            if target in text.lower():

                x1, y1 = bbox[0]
                x2, y2 = bbox[2]

                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)

                print(f"Found '{text}' at ({center_x}, {center_y})")
                print(f"Confidence: {confidence:.2f}")

                pyautogui.moveTo(center_x, center_y, duration=0.5)
                pyautogui.click()

                return True

        print("Text not found. Retrying...")
        time.sleep(2)

    print(f"\nText '{target}' not found on screen.")

    return False


# Optional manual test mode
if __name__ == "__main__":

    print("Capturing screen for manual test...")

    target = input("Enter text to click: ")

    success = find_and_click(target)

    if not success:
        print("Click operation failed.")