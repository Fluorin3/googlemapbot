import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains

import time

class Parser():

    def __init__(self, place, count):
        self.url = 'https://www.google.com/maps'
        self.count = count
        self.place = place
        self.list = []

    def parse(self):
        print(self.count)
        user = UserAgent()
        serivce = Service(executable_path=ChromeDriverManager().install())
        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument(f'--user-agent={user}')
        options.add_argument('--disable-blink-features=AutomationControlled')

        driver = webdriver.Chrome(service=serivce, options=options)
        driver.implicitly_wait(4)
        action = ActionChains(driver)

        driver.get(self.url)

        time.sleep(2)

        driver.find_element('class name', 'searchboxinput').send_keys(self.place)
        time.sleep(1)
        driver.find_element('xpath', '//button[@aria-label="Поиск"]').click()
        time.sleep(1)
        
        for i in range(int(self.count)):
            
            try:
                driver.find_elements("xpath", "//a[@class='hfpxzc']")[i].click()
                time.sleep(1)

                info = driver.find_elements('class name', 'AeaXub') # table info with status, code, addr, number, site
                info2 = driver.find_element('class name', 'F7nice ').text # Rating
                info3 = driver.find_element('xpath', '//h1[@class="DUwDvf lfPIob"]') # name
                
                self.list.append({'Адресс': info[0].text.replace('\ue0c8\n', ''), 
                                  'Plus-код': info[-1].text.replace('\uf186\n', ''), 
                                  'R': info2, 
                                  "name": info3.text, 
                                  'href': driver.current_url})
                time.sleep(1)
                driver.back()
                time.sleep(3)
            except:   
                info = driver.find_elements('class name', 'AeaXub') # table info with status, code, addr, number, site
                info2 = driver.find_element('class name', 'F7nice ').text # Rating
                info3 = driver.find_element('xpath', '//h1[@class="DUwDvf lfPIob"]') # name
                
                self.list.append({'Адресс': info[0].text.replace('\ue0c8\n', ''), 
                                  'Plus-код': info[-1].text.replace('\uf186\n', ''), 
                                  'R': info2, 
                                  "name": info3.text, 
                                  'href': driver.current_url})
                time.sleep(1)
                driver.back()
                time.sleep(3)
                
        driver.close()
        driver.quit()
            
    def get_answer(self):
        return self.list

class Review_Parser():

    def __init__(self, link, count):
        self.link = link
        self.count = count
        self.list = []
    
    def parse(self):
        user = UserAgent()
        serivce = Service(executable_path=ChromeDriverManager().install())
        options = ChromeOptions()

        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument(f'--user-agent={user}')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--lang=ru')

        driver = webdriver.Chrome(service=serivce, options=options)
        driver.fullscreen_window()
        driver.implicitly_wait(4)
        action = ActionChains(driver)

        driver.get(self.link)
        time.sleep(2)
        try:

            driver.find_element('xpath', '//button[@class="M77dve " and contains(@aria-label, "Ещё отзыв")]').click()
            print(200)
        except:
            print(404)
            
            
        time.sleep(2)
        buttons_more = driver.find_elements("xpath", "//button[@class='w8nwRe kyuRq']")
        for i in range(self.count):
            time.sleep(0.1)
            try:
                buttons_more[i].click()
            except:
                pass
        
    
        nicknames = driver.find_elements("class name", "d4r55 ")
        time.sleep(1)
        reviews = driver.find_elements("xpath", "//div[@class='GHT2ce']")
        time.sleep(1)
        rate = driver.find_elements("class name", "kvMYJc")
        time.sleep(1)
        for n in range(self.count):
            try:
                rate_str = rate[n].get_attribute('aria-label')[0]
                
                self.list.append({'nickname': nicknames[n].text, 'review': reviews[n].text, 'rate': rate_str})
                print('Словарь составлен!')
            except:
                print('Словарь НЕ составлен!')

        driver.close()
        driver.quit()
        
    def get_answer(self):
        return self.list