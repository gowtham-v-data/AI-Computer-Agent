import pyautogui
import time

def execute_steps(steps):

    for step in steps:

        step = step.lower().strip()

        # Skip empty lines
        if not step:
            continue

        print(f"\n=== Executing: {step} ===")

        # ---------------------------
        # OPEN BROWSER
        # ---------------------------
        if "open browser" in step:

            print("Opening Microsoft Edge browser...")

            pyautogui.press("win")
            time.sleep(1)

            pyautogui.write("edge")
            time.sleep(1)

            pyautogui.press("enter")

            time.sleep(6)

            print("✓ Browser opened")


        # ---------------------------
        # GO TO WEBSITE
        # ---------------------------
        elif "go to" in step:

            website = step.replace("go to", "").strip()

            print(f"Navigating to {website}...")

            time.sleep(1)

            # Focus address bar
            pyautogui.hotkey('ctrl', 'l')
            time.sleep(0.5)

            pyautogui.write(website, interval=0.05)
            pyautogui.press("enter")

            time.sleep(6)

            print(f"✓ Navigated to {website}")


        # ---------------------------
        # OPEN YOUTUBE
        # ---------------------------
        elif "youtube" in step:

            print("Navigating to YouTube...")

            time.sleep(1)

            # Focus address bar
            pyautogui.hotkey('ctrl', 'l')
            time.sleep(0.5)

            pyautogui.write("youtube.com", interval=0.05)
            pyautogui.press("enter")

            time.sleep(6)

            print("✓ YouTube page loaded")


        # ---------------------------
        # OPEN FILE EXPLORER
        # ---------------------------
        elif "open file explorer" in step or "file explorer" in step:

            print("Opening File Explorer...")

            pyautogui.press("win")
            time.sleep(1)

            pyautogui.write("file explorer")
            time.sleep(1)

            pyautogui.press("enter")

            time.sleep(3)

            print("✓ File Explorer opened")


        # ---------------------------
        # KAGGLE DOWNLOAD DATASET AS ZIP (SPECIAL CASE)
        # ---------------------------
        elif "download dataset as zip" in step.lower():

            print("Clicking 'Download dataset as zip' button...")
            
            # Wait for download menu to fully load after clicking Download button
            time.sleep(4)

            # Try OCR with very flexible matching
            found = False
            try:
                import easyocr
                import cv2
                import numpy as np

                print("Scanning for 'Download dataset as zip' option...")
                reader = easyocr.Reader(['en'], gpu=False)

                for attempt in range(3):
                    print(f"\nAttempt {attempt+1}/3...")

                    screenshot = pyautogui.screenshot()
                    img = np.array(screenshot)
                    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                    results = reader.readtext(img_bgr)

                    # Look for ANY text containing "Download dataset" or "dataset" + "zip"
                    best_match = None
                    best_score = 0
                    
                    for (bbox, text, confidence) in results:
                        text_lower = text.lower()
                        
                        # Score based on keyword matches
                        score = 0
                        if "download" in text_lower:
                            score += 3
                        if "dataset" in text_lower:
                            score += 4
                        if "zip" in text_lower or "kb" in text_lower or "12" in text_lower:
                            score += 3
                        
                        # Print candidates
                        if score > 0:
                            print(f"  Candidate: '{text}' (score: {score}, conf: {confidence:.2f})")
                        
                        # If this is the best match so far
                        if score >= 7 and score > best_score:
                            best_score = score
                            best_match = (bbox, text, confidence)
                    
                    if best_match:
                        bbox, text, confidence = best_match
                        x1, y1 = bbox[0]
                        x2, y2 = bbox[2]
                        
                        # Click slightly to the left to hit the icon/button area
                        center_x = int((x1 + x2) / 2) - 20
                        center_y = int((y1 + y2) / 2)
                        
                        print(f"\n✓ CLICKING: '{text}' at ({center_x}, {center_y})")
                        
                        pyautogui.moveTo(center_x, center_y, duration=0.5)
                        time.sleep(0.3)
                        pyautogui.click()
                        time.sleep(0.3)
                        
                        found = True
                        print("✓ Click completed!")
                        break

                    if not found and attempt < 2:
                        print("No match yet, retrying...")
                        time.sleep(2)

                if not found:
                    print("\n⚠️ OCR couldn't find the button. Trying mouse click at typical location...")
                    # Fallback: Click at a typical position where this button appears
                    # After clicking Download, the menu usually appears below it
                    screen_width, screen_height = pyautogui.size()
                    # Try clicking in the right-side area where Kaggle download menu typically appears
                    click_x = int(screen_width * 0.7)  # 70% from left
                    click_y = int(screen_height * 0.35)  # 35% from top
                    
                    print(f"Clicking estimated position: ({click_x}, {click_y})")
                    pyautogui.click(click_x, click_y)
                    print("✓ Fallback click executed")

            except Exception as e:
                print(f"Error: {e}")
                print("Using emergency fallback - tab and enter...")
                pyautogui.press('tab')
                time.sleep(0.3)
                pyautogui.press('enter')

            time.sleep(3)


        # ---------------------------
        # SEARCH VIDEO
        # ---------------------------
        elif "search" in step:

            search_term = step.replace("search", "").strip()

            print(f"Searching for: {search_term}")

            time.sleep(3)

            # YouTube shortcut to open search
            pyautogui.press('/')
            time.sleep(0.5)

            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.3)

            pyautogui.write(search_term, interval=0.05)

            time.sleep(0.5)

            pyautogui.press("enter")

            print(f"✓ Search completed for: {search_term}")

            time.sleep(6)


        # ---------------------------
        # RIGHT CLICK USING VISION (OCR)
        # ---------------------------
        elif "right click" in step:

            target = step.replace("right click", "").strip()

            print("Looking for (right-click):", target)

            try:
                import easyocr
                import cv2
                import numpy as np

                # Initialize OCR once
                reader = easyocr.Reader(['en'], gpu=False)

                found = False

                # Retry detection multiple times
                for attempt in range(5):

                    print(f"Vision attempt {attempt+1}...")

                    screenshot = pyautogui.screenshot()

                    img = np.array(screenshot)

                    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

                    results = reader.readtext(img_bgr)

                    # Print all detected text for debugging
                    print(f"\n--- Detected text (attempt {attempt+1}) ---")
                    for (bbox, text, confidence) in results:
                        print(f"  '{text}' (confidence: {confidence:.2f})")
                    print("---\n")

                    # Search for target - try flexible matching
                    for (bbox, text, confidence) in results:
                        # Remove all spaces, dots, and special chars for comparison
                        text_clean = text.lower().replace(" ", "").replace(".", "").replace(",", "").replace("(", "").replace(")", "")
                        target_clean = target.lower().replace(" ", "").replace(".", "").replace(",", "").replace("(", "").replace(")", "")
                        
                        # Multiple matching strategies
                        match = False
                        if target_clean in text_clean or text_clean in target_clean:
                            match = True
                        # Try matching key words for specific cases
                        elif "dataset" in target_clean and "zip" in target_clean:
                            if "dataset" in text_clean and "zip" in text_clean:
                                match = True
                        elif "download" in target_clean and "dataset" in target_clean:
                            if "download" in text_clean and "dataset" in text_clean:
                                match = True
                        
                        if match:

                            x1, y1 = bbox[0]
                            x2, y2 = bbox[2]

                            center_x = int((x1 + x2) / 2)
                            center_y = int((y1 + y2) / 2)

                            print(f"✓ Found match: '{text}' for target '{target}' at ({center_x}, {center_y})")

                            pyautogui.moveTo(center_x, center_y, duration=0.5)

                            pyautogui.rightClick()

                            found = True
                            break

                    if found:
                        break

                    time.sleep(2)

                if not found:
                    print(f"✗ Text '{target}' not found on screen after {attempt+1} attempts")

            except Exception as e:

                print("Right-click error:", e)

            time.sleep(3)


        # ---------------------------
        # CLICK EXTRACT BUTTON (Windows Dialog)
        # ---------------------------
        elif step.strip().lower() == "click extract":

            print("Clicking 'Extract' button in Windows extraction dialog...")
            
            time.sleep(3)

            try:
                import easyocr
                import cv2
                import numpy as np

                reader = easyocr.Reader(['en'], gpu=False)
                found = False

                for attempt in range(3):
                    print(f"\nAttempt {attempt+1}/3 - Looking for Extract button...")

                    screenshot = pyautogui.screenshot()
                    img = np.array(screenshot)
                    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                    results = reader.readtext(img_bgr)

                    print("All detected text:")
                    for (bbox, text, confidence) in results:
                        text_lower = text.strip().lower()
                        if "extract" in text_lower or "cancel" in text_lower or "browse" in text_lower:
                            print(f"  - '{text}' (conf: {confidence:.2f})")

                    # Look for "Extract" button - must NOT be "Extract all"
                    for (bbox, text, confidence) in results:
                        text_clean = text.strip().lower()
                        
                        # Match only "Extract" (not "Extract all" or other variations)
                        if text_clean == "extract":
                            x1, y1 = bbox[0]
                            x2, y2 = bbox[2]
                            center_x = int((x1 + x2) / 2)
                            center_y = int((y1 + y2) / 2)
                            
                            print(f"\n✓ Found Extract button at ({center_x}, {center_y})")
                            print("Moving mouse and clicking...")
                            
                            pyautogui.moveTo(center_x, center_y, duration=0.5)
                            time.sleep(0.5)
                            pyautogui.click()
                            time.sleep(0.3)
                            
                            found = True
                            print("✓ Extract button clicked!")
                            break

                    if found:
                        break
                    
                    time.sleep(1.5)

                if not found:
                    print("\n⚠️ Extract button not found via OCR.")
                    print("Trying alternative: Press Alt+E (Extract button shortcut)...")
                    pyautogui.hotkey('alt', 'e')
                    time.sleep(0.5)
                    
                    # If that doesn't work, try Tab+Enter
                    print("Also trying Tab+Enter as backup...")
                    pyautogui.press('tab')
                    time.sleep(0.3)
                    pyautogui.press('enter')
                    print("✓ Used keyboard shortcuts")

            except Exception as e:
                print(f"Error: {e}")
                print("Using Enter key fallback...")
                pyautogui.press('enter')

            time.sleep(3)


        # ---------------------------
        # CLICK USING VISION (OCR)
        # ---------------------------
        elif "click" in step:

            target = step.replace("click", "").strip()

            print("Looking for:", target)

            try:
                import easyocr
                import cv2
                import numpy as np

                # Initialize OCR once
                reader = easyocr.Reader(['en'], gpu=False)

                found = False

                # Retry detection multiple times
                for attempt in range(5):

                    print(f"Vision attempt {attempt+1}...")

                    screenshot = pyautogui.screenshot()

                    img = np.array(screenshot)

                    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

                    results = reader.readtext(img_bgr)

                    # Print all detected text for debugging (only on first attempt to reduce spam)
                    if attempt == 0:
                        print(f"\n--- Detected text ---")
                        for (bbox, text, confidence) in results[:20]:  # Show first 20
                            print(f"  '{text}' (confidence: {confidence:.2f})")
                        print("---\n")

                    # Search for target - try flexible matching
                    for (bbox, text, confidence) in results:
                        # Remove all spaces, dots, and special chars for comparison
                        text_clean = text.lower().replace(" ", "").replace(".", "").replace(",", "").replace("(", "").replace(")", "")
                        target_clean = target.lower().replace(" ", "").replace(".", "").replace(",", "").replace("(", "").replace(")", "")
                        
                        # Multiple matching strategies
                        match = False
                        if target_clean in text_clean or text_clean in target_clean:
                            match = True
                        # Try matching key words for specific cases
                        elif "dataset" in target_clean and "zip" in target_clean:
                            if "dataset" in text_clean and "zip" in text_clean:
                                match = True
                        elif "download" in target_clean and "dataset" in target_clean:
                            if "download" in text_clean and "dataset" in text_clean:
                                match = True
                        
                        if match:

                            x1, y1 = bbox[0]
                            x2, y2 = bbox[2]

                            center_x = int((x1 + x2) / 2)
                            center_y = int((y1 + y2) / 2)

                            print(f"✓ Found match: '{text}' for target '{target}' at ({center_x}, {center_y})")

                            pyautogui.moveTo(center_x, center_y, duration=0.5)

                            pyautogui.click()

                            found = True
                            break

                    if found:
                        break

                    time.sleep(2)

                if not found:
                    print(f"✗ Text '{target}' not found on screen after {attempt+1} attempts")

            except Exception as e:

                print("Click error:", e)

            time.sleep(3)


        # ---------------------------
        # CLICK FIRST VIDEO ON YOUTUBE
        # ---------------------------
        elif "first video" in step or "play first" in step:

            print("Looking for first video to click...")

            try:
                import easyocr
                import cv2
                import numpy as np

                reader = easyocr.Reader(['en'], gpu=False)
                
                time.sleep(2)
                screenshot = pyautogui.screenshot()
                img = np.array(screenshot)
                img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                
                # Save debug image
                cv2.imwrite("debug_screen.png", img_bgr)
                
                results = reader.readtext(img_bgr)
                
                # Find video titles (they appear at the top of search results)
                # YouTube videos typically have larger text that's clickable
                video_candidates = []
                
                for (bbox, text, confidence) in results:
                    # Look for substantial text that could be video titles
                    if len(text.strip()) > 10 and confidence > 0.3:
                        y_position = bbox[0][1]  # Get Y coordinate
                        video_candidates.append((y_position, bbox, text))
                
                if video_candidates:
                    # Sort by Y position (top to bottom) and click the first one
                    video_candidates.sort(key=lambda x: x[0])
                    
                    # Click the first video (skip if it's too high, might be header)
                    for y_pos, bbox, text in video_candidates:
                        if y_pos > 150:  # Skip header elements
                            x1, y1 = bbox[0]
                            x2, y2 = bbox[2]
                            center_x = int((x1 + x2) / 2)
                            center_y = int((y1 + y2) / 2)
                            
                            print(f"Clicking first video: '{text}'")
                            pyautogui.moveTo(center_x, center_y, duration=0.5)
                            pyautogui.click()
                            print("✓ First video clicked")
                            break
                else:
                    print("No video titles detected")
                    
            except Exception as e:
                print(f"First video click error: {e}")
            
            time.sleep(3)


        # ---------------------------
        # READ/DETECT SCREEN TEXT
        # ---------------------------
        elif "read screen" in step or "detect screen" in step or "show screen" in step:

            print("Reading screen text...")

            try:
                import easyocr
                import cv2
                import numpy as np

                reader = easyocr.Reader(['en'], gpu=False)
                
                screenshot = pyautogui.screenshot()
                img = np.array(screenshot)
                img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                
                results = reader.readtext(img_bgr, detail=0)
                
                print("\n" + "="*50)
                print("DETECTED SCREEN TEXT:")
                print("="*50)
                for text in results:
                    if text.strip():
                        print(f"  • {text}")
                print("="*50 + "\n")
                
            except Exception as e:
                print(f"Screen reading error: {e}")
            
            time.sleep(1)


        # ---------------------------
        # TYPE TEXT
        # ---------------------------
        elif step.startswith("type "):

            text_to_type = step.replace("type", "", 1).strip()
            
            print(f"Typing: {text_to_type}")
            
            pyautogui.write(text_to_type, interval=0.05)
            
            time.sleep(0.5)
            
            print("✓ Text typed")


        # ---------------------------
        # PRESS KEY
        # ---------------------------
        elif step.startswith("press "):

            key = step.replace("press", "", 1).strip()
            
            print(f"Pressing key: {key}")
            
            pyautogui.press(key)
            
            time.sleep(0.5)
            
            print(f"✓ Pressed {key}")


        elif "kaggle" in step and "dataset" in step:
            from kaggle_browser_downloader import download_kaggle_dataset

            dataset = step.replace("open kaggle","").replace("search","").replace("dataset","").strip()

            download_kaggle_dataset(dataset)