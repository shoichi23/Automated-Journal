import pyautogui
import time
from pywinauto import Application
from datetime import date, datetime
import psutil
import requests
from bs4 import BeautifulSoup

# Today's date
today = date.today()

# Define function for centering, moving, and clicking on the image
def uiclick(res, delay=1):
    ui = pyautogui.center(res)
    pyautogui.moveTo(ui)
    pyautogui.click(ui)
    time.sleep(delay)

# Check if the application is running and end the task
app_name = "Notion.exe"
for proc in psutil.process_iter():
    if proc.name() == app_name:
        proc.kill()
        print(f"Closed the running {app_name} process.")

# Start the application
app_path = r"C:\Users\syout\AppData\Local\Programs\Notion\Notion.exe"
app = Application().start(app_path)

# Wait for the main window to appear
timeout = 10  # Maximum time to wait (in seconds)
start_time = time.time()

while time.time() - start_time < timeout:
    main_window = app['Notion']
    if main_window.exists():
        print("Notion has loaded.")
        break

time.sleep(5)  # Adjust the delay as needed

# Predefined image files with confidence levels
image_files = [
    ("5MinuteJournal.png", 0.8),
    ("Drop.png", 0.8),
    ("DailyTemplete.png", 0.9),
    ("Day.png", 0.9),
    ("Date.png", 0.9),
    ("Quote.png", 0.9)
]

for image_file, confidence in image_files:
    # Locate the image on the screen with the specified confidence level
    res = pyautogui.locateOnScreen(image_file, confidence=confidence)

    # Check if the image was found
    if res is not None:
        # Perform UI click action
        uiclick(res)

        # Delay
        time.sleep(0.7)

        # Enter text for Day.png
        if image_file == "Day.png":
            current_day = today.strftime("%a")
            uiclick(res, delay=0.2)
            pyautogui.write(current_day)
            time.sleep(0.2)
            pyautogui.press("enter")
            time.sleep(0.2)

        # Enter text for Date.png
        if image_file == "Date.png":
            uiclick(res)
            datebox = pyautogui.locateOnScreen("Datebox.png", confidence=confidence)
            
            if datebox is not None:
                # Delete default date
                def hold_Del(hold_time):
                    start = time.time()
                    while time.time() - start < hold_time:
                        pyautogui.press('backspace')
                hold_Del(5)
                # Enter the current date
                current_date = today.strftime("%m/%d/%Y")
                print(current_date)
                pyautogui.write(current_date)
                time.sleep(0.2)

                # Press the Enter key
                pyautogui.press("enter")
                time.sleep(0.2)
                
                # Press the Esc key
                pyautogui.press("esc")

        # Enter text for Quote.png
        if image_file == "Quote.png":
            # Send a GET request to the website that provides the quote of the day
            url = "https://www.brainyquote.com/quote_of_the_day"
            response = requests.get(url)

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")

            # Find the element that contains the quote of the day
            quote_element = soup.find("a", {"title": "view quote"})

            # Check if the quote element was found
            if quote_element is not None:
                # Extract the text of the quote
                quote_text = quote_element.text.strip()

                # Perform UI click action
                uiclick(res, delay=0.2)
                time.sleep(0.2)
                pyautogui.write(quote_text)
                pyautogui.press("enter")

    else:
        print(f"Image '{image_file}' not found on the screen.")
        exit()  # Exit the program if the timeout is reached


if time.time() - start_time >= timeout:
    print("Timeout: Notion did not load within the specified time.")
    exit()  # Exit the program if the timeout is reached
