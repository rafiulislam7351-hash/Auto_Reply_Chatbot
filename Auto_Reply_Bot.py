import os
import re
import time
import random
import pyautogui
import pyperclip
from openai import OpenAI
from dotenv import load_dotenv

# 1. Security: Load API Key from environment variables
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"

if not API_KEY:
    print("Error: OPENROUTER_API_KEY not found. Please set it in a .env file.")
    exit()

# Safety: Move mouse to any corner to kill the script
pyautogui.FAILSAFE = True

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)


def human_typing(text):
    """Types text with random delays to mimic a human."""
    for char in text:
        pyautogui.write(char)
        time.sleep(random.uniform(0.03, 0.1))


def get_ai_response(captured_text):
    if not captured_text.strip():
        return None

    try:
        completion = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=[
                {
                    "role": "system",
                    "content": "You are Rafiul, a Data Science student. Speak naturally, use lowercase occasionally, be conversational."
                },
                {"role": "user", "content": captured_text}
            ]
        )
        full_content = completion.choices[0].message.content
        # Remove thinking tags
        clean_response = re.sub(r'<think>.*?</think>', '', full_content, flags=re.DOTALL).strip()
        return clean_response
    except Exception as e:
        print(f"API Error: {e}")
        return "my internet is acting up, one sec..."


def find_chat_box():
    """
    Finds the chat input box using an image anchor.
    Requires 'anchor.png' (a screenshot of the chat text box or send button).
    """
    try:
        # Search for the chatbox image on screen
        location = pyautogui.locateOnScreen('anchor.png', confidence=0.8)
        if location:
            return pyautogui.center(location)
    except Exception as e:
        print(f"UI Search Error: {e}")
    return None


def main_flow():
    print("--- Rafiul AI Automator (Public Version) ---")
    print("Ensure 'anchor.png' is in the script folder.")

    # 1. Locate UI
    target = find_chat_box()
    if not target:
        print("Could not find the chat window. Make sure it's visible on screen.")
        return

    # 2. Capture Logic (Simplified for public use)
    # Instead of dragging, we assume the user has the window active
    print("Capturing latest message...")
    pyautogui.click(target.x, target.y - 100)  # Click slightly above the chatbox to focus
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(1)

    input_text = pyperclip.paste()

    # 3. AI Processing
    print("Rafiul is thinking...")
    reply = get_ai_response(input_text)

    if reply:
        # Simulate reading/prep time
        time.sleep(random.uniform(2, 5))

        # 4. Reply
        pyautogui.click(target)  # Click the chatbox found via image
        print(f"Sending: {reply[:30]}...")

        if len(reply) < 120:
            human_typing(reply)
        else:
            pyperclip.copy(reply)
            pyautogui.hotkey('ctrl', 'v')

        time.sleep(0.5)
        pyautogui.press('enter')
        print("Done.")


if __name__ == "__main__":
    try:
        main_flow()
    except KeyboardInterrupt:
        print("\nStopped.")