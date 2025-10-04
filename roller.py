import pyautogui
import keyboard
import time
import random
import os

pyautogui.PAUSE = 0.3
pyautogui.FAILSAFE = True

# ---------------- CONFIG ----------------
DESIRED_ITEMS_FOLDER = "C:\Users\rdsou\Downloads\rollerdata"  # each file is a picture of an item in shop
REFRESH_BUTTON_IMG   = "refresh_button.PNG"
CONFIRM_BUTTON_IMG   = "confirm_button.PNG"
BUY_BUTTON_COV_IMG       = "buy_button_covenant.PNG"
BUY_BUTTON_MYM_IMG       = "buy_button_mystic.PNG"

SCROLL_DISTANCE = 350

def random_offset():
    return random.randint(-2, 2)

def locate(image_file, confidence=0.90):
    return pyautogui.locateOnScreen(image_file, confidence=confidence)

def click_center(region):
    center = pyautogui.center(region)
    pyautogui.click(center.x + random_offset(), center.y + random_offset())

def click_price_area(region):
    # Click on right side (price) — adjust offset as needed for your game UI
    x_click = region.left + region.width - 40 + random_offset()  # 40px from right edge
    y_click = region.top + region.height / 2 + random_offset()
    pyautogui.click(x_click, y_click)

def buy_item_flow(item_img):
    found = locate(item_img, confidence=0.90)
    if found:
        print(f"[+] Desired item found: {item_img}")
        click_price_area(found)
        time.sleep(0.4)
        buy_btn = locate(BUY_BUTTON_IMG, confidence=0.90)
        if buy_btn:
            click_center(buy_btn)
            print(f"    Purchased {item_img}")
            time.sleep(0.5)
        else:
            print("    Buy button not found!")
        return True
    return False

# Load all desired item images
desired_items = [
    os.path.join(DESIRED_ITEMS_FOLDER, f)
    for f in os.listdir(DESIRED_ITEMS_FOLDER)
    if f.lower().endswith((".png", ".jpg"))
]

print("Press 'q' to quit bot.")
time.sleep(2)

while not keyboard.is_pressed('q'):

    # Step 1: Refresh shop
    refresh_btn = locate(REFRESH_BUTTON_IMG)
    if refresh_btn:
        click_center(refresh_btn)
        time.sleep(0.4)
        confirm_btn = locate(CONFIRM_BUTTON_IMG)
        if confirm_btn:
            click_center(confirm_btn)
            print("[*] Shop refreshed.")
            time.sleep(0.6)

    # Step 2: Check first 4 items
    for img in desired_items:
        buy_item_flow(img)

    # Step 3: Scroll to bottom 2 items
    screen_w, screen_h = pyautogui.size()
    pyautogui.moveTo(screen_w // 2, screen_h // 2)
    pyautogui.dragRel(0, -SCROLL_DISTANCE, duration=0.3)
    time.sleep(0.4)

    # Step 4: Check bottom 2
    for img in desired_items:
        buy_item_flow(img)

    # Scroll back up
    pyautogui.dragRel(0, SCROLL_DISTANCE, duration=0.3)
    time.sleep(0.5)

print("Exited successfully.")
