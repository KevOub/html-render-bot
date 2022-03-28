import os
from time import sleep
import random
import string
from flask import Flask, flash, redirect, request, url_for, send_from_directory
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/app/html-files/'
DOWNLAOD_FOLDER = '/app/screenshots/'
ALLOWED_EXTENSIONS = {'html'}
WINDOW_SIZE = "1920,1080"

Flask.secret_key = "test"

# send file

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def set_chrome_options():
    """Sets chrome options for Selenium.

    Chrome options for headless browser is enabled.

    """

    chrome_options = Options()

    chrome_options.add_argument("window-size=1980,960")

    chrome_options.add_argument("--headless")

    # chrome_options.add_argument("--screenshot")
    #
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)

    chrome_options.add_argument("--no-sandbox")

    # chrome_options.add_argument("--disable-xss-auditor")

    chrome_options.add_argument("--disable-web-security")

    chrome_options.add_argument("--disable-dev-shm-usage")

    chrome_prefs = {}

    chrome_options.experimental_options["prefs"] = chrome_prefs

    chrome_prefs["profile.default_content_settings"] = {"images": 2}

    return chrome_options




def generateFilename(N = 8):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

def screenshot(html_content: str, filename : str):
    # launch headless chrome
    browser = webdriver.Chrome(options=set_chrome_options())

    # load html file
    # browser.get("https://google.com")

    browser.get(
        f"data:text/html;charset=utf-8,{html_content}")
    # browser.set_window_size(100, 100)

    browser.find_element_by_tag_name('body').screenshot(
        f"{DOWNLAOD_FOLDER}{filename}.png")  # avoids scrollbar

    browser.quit()
    # TODO return path of file
    return f"{filename}.png"


project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, './templates')
app = Flask(__name__, template_folder=template_path)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/files/<path:path>")
def get_file(path):
    """Download a file."""
    # return send_from_directory(DOWNLAOD_FOLDER, path, as_attachment=True)
    return f"<img src=\"/files/{path}\">"


@app.route("/", methods=["GET", "POST"])
def api_call():
    if request.method == "GET":
        return "Screenshot requires POST to / with html content"
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            print(file.read().decode())
            print(f"TAKING SCREENSHOT OF {file.filename}!")
            fileout = screenshot(file.read().decode(),generateFilename())
            # filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return "redirect(url_for('download_file', name=filename))"
            return fileout
        else:
            print("OOP!")
            return "404"


if __name__ == "__main__":
    app.run(host='0.0.0.0')
