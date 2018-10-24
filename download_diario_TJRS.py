# -*- coding: utf-8 -*-
import datetime
import os

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

today = str(datetime.datetime.now().strftime("%Y%m%d"))

options = webdriver.ChromeOptions() 
options.add_experimental_option("prefs", {
  "download.default_directory": os.path.join(r"C:\Temp\PDF", today),
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,   
  "safebrowsing.enabled": True
})
chromepath = "C:\\Temp\\chromedriver_win32\\chromedriver.exe"
browser=webdriver.Chrome(executable_path=chromepath, chrome_options=options)

browser.get("http://www1.tjrs.jus.br/busca/?tb=dj")
browser.implicitly_wait(5)
main_window  = browser.current_window_handle

link = browser.find_element_by_xpath("""//*[@id="rollover-target-list"]/li[1]/ul/li[3]/a""")
elements = browser.find_elements_by_class_name("rollover-target-list-link")

for element in elements :
    element.click()
    WebDriverWait(browser, 10).until(EC.number_of_windows_to_be(2))
    windows_after = browser.window_handles
    new_window = [x for x in windows_after if x != main_window][0]
    
    browser.switch_to_window(new_window)
    
    link_download_pdf = browser.find_element_by_xpath("/html/body/div/form/table/tbody/tr/td[6]/div/a")
    link_download_pdf.click()

    browser.switch_to_window(main_window)


browser.implicitly_wait(20)

browser.quit()
browser.close()