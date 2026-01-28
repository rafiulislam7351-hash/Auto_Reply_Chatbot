import pyautogui
import sys

print("--- Rafiul's Coordinate Finder ---")
print("Move your mouse to the target area. Press Ctrl+C to stop.")

try:
    while True:
        # Get current mouse position
        x, y = pyautogui.position()

        # \r allows us to overwrite the same line in the terminal
        position_str = f"X: {str(x).rjust(4)}  Y: {str(y).rjust(4)}"
        print(position_str, end="")
        print("\b" * len(position_str), end="", flush=True)

except KeyboardInterrupt:
    print(f"\nFinal Position Saved: {pyautogui.position()}")
    print("Done.")