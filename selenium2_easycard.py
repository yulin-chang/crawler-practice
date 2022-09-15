import sys
import getopt
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd


SEARCH_URL = 'https://ezweb.easycard.com.tw/search/CardSearch.php'


def print_usage():
   print('輸入錯誤! 請輸入卡片外觀卡號與生日! ')
   print('python selenium2_easycard.py OPTIONS')
   print('OPTIONS:')
   print('{:>6} {:<12} {}'.format('-c','cardno', 'Input CardNo'))
   print('{:>6} {:<12} {}'.format('-b','birthday', 'Input Birthday'))


class Card():
    def __init__(self, cardno, birthday):
        self.cardno = cardno
        self.birthday = birthday
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), 
                            options=Options().add_experimental_option("detach", True))
        self.data = []
        self.sub_data = []
        self.col_name = []

    def run(self):
        self.get_browser()
        self.enter_card_no()
        self.enter_birthday()
        self.select_date_range()
        self.wait_robot_check()
        self.click_search()
        self.get_result()
        self.output_file()

    def get_browser(self):
        self.driver.get(SEARCH_URL)

    def enter_card_no(self):
        # text
        txt_card_no = self.driver.find_element(By.XPATH, '/html/body/form/div/div[1]/div[2]/div[2]/div[1]/ul/li[1]/input')
        txt_card_no.send_keys(self.cardno)

    def enter_birthday(self):
        # text
        txt_birthday = self.driver.find_element(By.XPATH, '/html/body/form/div/div[1]/div[2]/div[2]/div[1]/ul/li[2]/input')
        txt_birthday.send_keys(self.birthday) 

    def select_date_range(self):
        # radio 
        radio_range = self.driver.find_element(By.ID, 'date3m')
        radio_range.send_keys(Keys.SPACE) 

    def wait_robot_check(self):
        input('need to press enter after done with robot check')    

    def click_search(self):
        # button
        self.driver.find_element(By.ID, 'btnSearch').click()

    def get_result(self):
        # wait
        self.driver.implicitly_wait(5) # seconds

        # get title 
        self.col_name = self.driver.find_element(By.ID, 'pgh').text.split(' ')

        # get record
        record = self.driver.find_elements(By.CLASS_NAME, 'r1')
        for r in record:
            self.sub_data = r.text.split(' ')
            self.sub_data[0:2] = [''.join(self.sub_data[0:2])]
            self.data.append(self.sub_data)


    def output_file(self):
        df = pd.DataFrame(self.data, columns=self.col_name)
        df.to_csv('output_card_record.csv', index=False)
        # df.to_excel('output_card_record.xlsx', index=False)
        

if __name__ == '__main__':
    
    try:
        opts, args = getopt.getopt(sys.argv[1:],"c:b:",["cardno=","birthday="])
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)

    cardno = None
    birthday = None
    for opt, arg in opts:
        if opt in ("-c", "--cardno"):
            cardno = arg
        elif opt in ("-b", "--birthday"):
            birthday = arg

    if not cardno or not birthday:
        print_usage()
        sys.exit(2)

    c = Card(cardno, birthday)
    c.run()

