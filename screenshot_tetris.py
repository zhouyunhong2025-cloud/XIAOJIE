#!/usr/bin/env python3
"""
Screenshot the Tetris game from index.html
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--window-size=1200,800')
chrome_options.add_argument('--disable-gpu')

try:
    # Create webdriver
    driver = webdriver.Chrome(options=chrome_options)
    
    # Load the HTML file
    html_path = os.path.abspath('/workspaces/XIAOJIE/I.QUEUE/index.html')
    driver.get(f'file://{html_path}')
    
    # Wait for Tetris canvas to render
    print("Waiting for canvas to render...")
    wait = WebDriverWait(driver, 10)
    canvas = wait.until(EC.presence_of_element_located((By.ID, 'tetrisCanvas')))
    
    # Wait a bit more for animation
    time.sleep(3)
    
    # Take screenshot
    screenshot_path = '/workspaces/XIAOJIE/docs/tetris-demo.png'
    driver.save_screenshot(screenshot_path)
    print(f"✓ Screenshot saved: {screenshot_path}")
    
    driver.quit()
    print("Done!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
