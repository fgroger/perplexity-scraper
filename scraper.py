from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape_perplexity():
    data = request.get_json()
    query = data.get('query')

    # Set up headless Chrome (using Replit’s Puppeteer/Playwright Docker image)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://www.perplexity.ai/")

        # Wait for page load
        time.sleep(3)

        search_box = driver.find_element(By.TAG_NAME, "textarea")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        # Wait for Perplexity response to appear
        time.sleep(7)

        results = driver.find_elements(By.CSS_SELECTOR, ".markdown")
        answer = results[0].text if results else "No result found."

        return jsonify({"result": answer})
    finally:
        driver.quit()

app.run(host="0.0.0.0", port=81)
