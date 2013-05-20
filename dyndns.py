from selenium import webdriver
import datetime
import syslog
import traceback
import StringIO
import sys
import os
import pyvirtualdisplay
import json

# Load config
home = os.path.expanduser("~")
config_file = os.path.join(home, ".config/dyndns.json")
try:
    with open(config_file, "rb") as fp:
        config = json.load(fp)
except IOError:
    error = "You need to set up a configuration file with your DynDNS username " \
            "and password!\n" \
            'The path of the file must be '+config_file+"\n"+ \
            "Check dyndns.json.example for an example."
    syslog.syslog(syslog.LOG_ERR, "DynDNS bot is not configured!")
    for line in error.split('\n'):
        syslog.syslog(syslog.LOG_ERR, line)
    sys.stderr.write(error+'\n')
    exit(1)

username = config['username']
password = config['password']
screenshots_path = os.path.expanduser(config['screenshots_path'])

if not os.path.exists(screenshots_path):
    os.makedirs(screenshots_path)

visible = '-v' in sys.argv

def report_error():
    exc = traceback.format_exc()
    syslog.syslog(syslog.LOG_ERR, "DynDNS bot stopped working!")
    for line in exc.split('\n'):
        syslog.syslog(syslog.LOG_ERR, line)
    sys.stderr.write(exc)

try:
    display = pyvirtualdisplay.Display(visible=visible, size=(1024, 768))
    display.start()
except:
    report_error()
    sys.exit(1)

try:
    # Create a new instance of the Firefox driver
    driver = webdriver.Firefox()
except:
    report_error()
    sys.exit(1)

try:
    # Log in DynDNS
    driver.get("https://account.dyn.com/entrance/")

    username_field = driver.find_element_by_css_selector('#loginbox input[name="username"]')
    username_field.send_keys(username)

    password_field = driver.find_element_by_css_selector('#loginbox input[name="password"]')
    password_field.send_keys(password)

    password_field.submit() # Press Enter

    # Take a screenshot
    driver.get_screenshot_as_file(os.path.join(
        screenshots_path,
        'dyndns-%s.png' % datetime.datetime.now().isoformat()
        ))

    # Done, log out
    log_out_button = driver.find_element_by_link_text('Log Out')
    log_out_button.click()

    syslog.syslog("DynDNS bot logged in successfully!")
except:
    report_error()

finally:
    driver.quit()
    display.stop()
