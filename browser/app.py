import base64
import os
from time import sleep

from flask import Flask, request, flash, redirect,url_for
from selenium import webdriver
from selenium.common.exceptions import (NoAlertPresentException,
                                        TimeoutException,
                                        UnexpectedAlertPresentException)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/app/html-files/'
ALLOWED_EXTENSIONS = {'html', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
WINDOW_SIZE = "1920,1080"

Flask.secret_key = "test"

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


FILE = "file://main.html"


# def fire(browser,payload):
#     browser.execute_script("document.write('{}')".format(payload))
#     print("TEST: {}".format(browser.switch_to.alert.text ))
#     return browser.switch_to.alert.text != None


def screenshot(html_content: str):
    # launch headless chrome
    browser = webdriver.Chrome(options=set_chrome_options())

    # load html file
    # browser.get("https://google.com")

    browser.get(
        "data:text/html;charset=utf-8,{html_content}".format(html_content=html_content))
    # browser.set_window_size(100, 100)

    browser.find_element_by_tag_name('body').screenshot(
        "/app/uploads/test.png")  # avoids scrollbar

    browser.quit()
    # TODO return path of file
    return


project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, './templates')
app = Flask(__name__, template_folder=template_path)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def api_call():
    if request.method == "GET":
        # driver = webdriver.Chrome(options=set_chrome_options())
        screenshot("")
        # return render_template('flag.html')
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
        if file and allowed_file(file.filename):
            # print(file.stream.read())
            screenshot(file.stream.read())
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return "redirect(url_for('download_file', name=filename))"
            return "success!"


if __name__ == "__main__":
    app.run(host='0.0.0.0')
