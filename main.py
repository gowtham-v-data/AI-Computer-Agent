from google import genai
from google.genai import types
import warnings
from computer_executor import execute_steps
import time
import re

# Suppress deprecation warnings
warnings.filterwarnings('ignore', category=FutureWarning)

API_KEY = "AIzaSyAVbaO9Sety2NH8WrS6QAVc3M_BZLnQARI"

client = genai.Client(api_key=API_KEY)

def generate_plan_from_command(command):
    """Generate automation plan based on command patterns (no API needed)"""
    cmd_lower = command.lower()
    
    # Email pattern
    if "email" in cmd_lower or "mail" in cmd_lower:
        # Extract email and message
        email_match = re.search(r'(\S+@\S+\.\S+)', command)
        email = email_match.group(1) if email_match else "example@gmail.com"
        
        # Extract message after "saying" or "message"
        message = ""
        if "saying" in cmd_lower:
            message = command.split("saying", 1)[1].strip()
        elif "message" in cmd_lower:
            message = command.split("message", 1)[1].strip()
        else:
            message = "hello"
        
        return f"""open browser
go to gmail.com
click Compose
type {email}
press tab
press tab
type {message}
click Send"""
    
    # YouTube pattern
    elif "youtube" in cmd_lower:
        # Extract search term
        search_term = ""
        if "search" in cmd_lower:
            parts = cmd_lower.split("search")
            if len(parts) > 1:
                search_term = parts[1].strip()
                # Remove "and play", "first video", etc.
                search_term = re.sub(r'\s+(and|play|first|video|click).*', '', search_term).strip()
        
        if not search_term and "open youtube" in cmd_lower:
            # Extract what comes after "youtube"
            after_youtube = cmd_lower.split("youtube", 1)[1].strip()
            search_term = re.sub(r'^(and|search|for|a)\s+', '', after_youtube).strip()
        
        plan = f"""open browser
go to youtube.com"""
        if search_term:
            plan += f"""
search {search_term}"""
            if "play" in cmd_lower or "first" in cmd_lower:
                plan += """
click first video"""
        return plan
    
    # Kaggle download pattern
    elif "kaggle" in cmd_lower and ("download" in cmd_lower or "dataset" in cmd_lower):
        # Extract dataset name
        dataset_name = "dataset"
        if "titanic" in cmd_lower:
            dataset_name = "titanic"
        elif "iris" in cmd_lower:
            dataset_name = "iris"
        else:
            # Try to extract dataset name
            words = cmd_lower.split()
            for i, word in enumerate(words):
                if word in ["dataset", "data"] and i > 0:
                    dataset_name = words[i-1]
                    break
        
        return f"""open browser
go to kaggle.com
click Datasets
search {dataset_name} dataset
click {dataset_name}
click Download
click Download dataset as zip
open file explorer
click Downloads
right click archive.zip
click Extract all
click Extract"""
    
    # Generic browser + search pattern
    elif "search" in cmd_lower:
        search_term = cmd_lower.split("search", 1)[1].strip()
        return f"""open browser
search {search_term}"""
    
    # Generic website visit
    elif "go to" in cmd_lower or ".com" in cmd_lower or ".org" in cmd_lower:
        # Extract website
        website_match = re.search(r'(\S+\.(com|org|net|edu|io))', command)
        if website_match:
            website = website_match.group(1)
        else:
            website = cmd_lower.split("go to", 1)[1].strip() if "go to" in cmd_lower else "google.com"
        
        return f"""open browser
go to {website}"""
    
    # Default: just open browser
    else:
        return "open browser"

print("=" * 50)
print("AI Computer Agent")
print("=" * 50)
command = input("Enter your command: ")

prompt = f"""
Convert the command into detailed automation steps using these patterns:
- "open browser" - opens web browser (Edge)
- "go to <website>" - navigates to a specific website (e.g., "go to kaggle.com", "go to youtube.com")
- "youtube" - navigates to YouTube.com  
- "search <term>" - searches for something on current page
- "read screen" - reads and displays all text on screen
- "click first video" - clicks the first video in search results
- "click <text>" - finds and clicks specific text on screen (e.g., "click Datasets", "click titanic", "click Download", "click Download dataset as zip")
- "right click <text>" - finds and right-clicks specific text on screen
- "type <text>" - types text (e.g., "type hello world", "type john@gmail.com")
- "press <key>" - presses a keyboard key (e.g., "press tab", "press enter")
- "open file explorer" - opens Windows File Explorer
- "click Downloads" - navigates to Downloads folder
- "send email to <email> saying <message>" - opens Gmail and sends email via browser

Rules:
- Return ONLY the step commands
- Each step on a new line
- Be DETAILED and EXPLICIT - break down into EVERY small step
- Always specify website navigation with "go to <website>"
- For Kaggle: ALWAYS click "Datasets" in sidebar BEFORE searching
- For Kaggle downloads: Click "Download" button, THEN click "Download dataset as zip"
- After downloading: open file explorer, go to Downloads, click the zip file, click Extract all
- Include EVERY necessary click (sidebar, search results, buttons)
- No numbers, no explanations, no extra text

Examples:

Command: open youtube and search python tutorial
Steps:
open browser
go to youtube.com
search python tutorial

Command: download titanic dataset from kaggle
Steps:
open browser
go to kaggle.com
click Datasets
search titanic dataset
click titanic
click Download
click Download dataset as zip
open file explorer
click Downloads
right click archive.zip
click Extract all
click Extract

Command: find iris dataset on kaggle and download it
Steps:
open browser
go to kaggle.com
click Datasets
search iris dataset
click iris
click Download
click Download dataset as zip
open file explorer
click Downloads
right click archive.zip
click Extract all
click Extract

Command: send email to viji29783@gmail.com saying hello
Steps:
open browser
go to gmail.com
click Compose
type viji29783@gmail.com
press tab
press tab
type hello
click Send

Command: open youtube search AI and play first video
Steps:
open browser
go to youtube.com
search AI
click first video

Command: send email to john@example.com saying project completed
Steps:
open browser
go to gmail.com
click Compose
type john@example.com
press tab
press tab
type project completed
click Send

Command: {command}
Steps:
"""

# Try to generate plan with API
try:
    response = client.models.generate_content(
        model='gemini-1.5-flash',
        contents=prompt
    )

    # Handle blocked/empty responses
    try:
        plan = response.text
    except (ValueError, AttributeError) as e:
        print(f"\n⚠️ API response blocked or empty, using built-in plan generator...")
        plan = generate_plan_from_command(command)

except Exception as e:
    # API failed - use built-in plan generator
    print(f"\n⚠️ API not available, using built-in plan generator...")
    plan = generate_plan_from_command(command)

print("\nGenerated Plan:\n")
print(plan)

steps = plan.split("\n")

execute_steps(steps)