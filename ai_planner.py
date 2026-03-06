import google.generativeai as genai
import warnings

# Suppress the deprecation warning
warnings.filterwarnings('ignore', category=FutureWarning)

genai.configure(api_key="AIzaSyAVbaO9Sety2NH8WrS6QAVc3M_BZLnQARI")

model = genai.GenerativeModel("gemini-1.5-flash")

def plan_task(command):

    prompt = f"""
Convert the command into detailed automation steps using these patterns:
- "open browser" - opens web browser (Edge)
- "go to <website>" - navigates to a specific website (e.g., "go to kaggle.com", "go to youtube.com")
- "youtube" - navigates to YouTube.com  
- "search <term>" - searches for something on current page
- "read screen" - reads and displays all text on screen
- "click first video" - clicks the first video in search results
- "click <text>" - finds and clicks specific text on screen (e.g., "click titanic", "click download")
- "type <text>" - types text into a text field

Rules:
- Return ONLY the step commands
- Each step on a new line
- Be DETAILED and EXPLICIT - break down into small steps
- Always specify website navigation with "go to <website>"
- Always include all necessary clicks
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
search titanic dataset
click titanic
click download

Command: open youtube search AI and play first video
Steps:
open browser
go to youtube.com
search AI
click first video

Command: find the iris dataset on kaggle
Steps:
open browser
go to kaggle.com
search iris dataset
click iris

Command: {command}
Steps:
"""

    response = model.generate_content(prompt)

    return response.text


command = input("Enter your command: ")

steps = plan_task(command)

print("\nAI Plan:\n")
print(steps)