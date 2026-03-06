import speech_recognition as sr
from agent_brain import create_plan
from computer_executor import execute_steps

recognizer = sr.Recognizer()

def listen_command():

    with sr.Microphone() as source:

        print("Listening...")

        audio = recognizer.listen(source)

        try:

            command = recognizer.recognize_google(audio)

            print("You said:", command)

            return command

        except:

            print("Could not understand audio")

            return None


def run_voice_agent():

    command = listen_command()

    if command:

        print("\nPlanning task...\n")

        steps = create_plan(command)

        for step in steps:
            print("•", step)

        print("\nExecuting...\n")

        execute_steps(steps)


if __name__ == "__main__":

    run_voice_agent()