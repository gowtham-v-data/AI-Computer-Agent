import pyautogui
from PIL import Image
import easyocr

# Initialize EasyOCR reader (first time will download the model)
print("Initializing OCR engine...")
reader = easyocr.Reader(['en'], gpu=False)

# Capture screen
print("Capturing screenshot...")
screenshot = pyautogui.screenshot()

# Save screenshot
screenshot.save("screen.png")

# Read text using EasyOCR
print("Reading text from screen...")
result = reader.readtext("screen.png", detail=0)

# Join all detected text
text = '\n'.join(result)

print("\nDetected Screen Text:\n")
print(text)
