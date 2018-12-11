#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
#options.headless = True
options.set_headless(True)

#browser = webdriver.Chrome(executable_path='/usr/lib64/chromium/chromedriver')
browser = webdriver.Firefox(options=options)
browser.get('https://www.google.com')
print( browser.title )
#print( browser.findElements(By.CLASS_NAME("szppmdbYutt__middle-slot-promo")) )
browser.quit()

