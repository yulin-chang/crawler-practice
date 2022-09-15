from datetime import datetime, timedelta
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


SEARCH_URL = 'https://www.thsrc.com.tw/'
INPUT_LOCATION1 = '台北'
INPUT_LOCATION2 = '台南'
INPUT_HOUR = '14'


class HSR:
    def __init__(self):
        self.driver = None
    
    def run(self):
        self.get_browser()
        self.auto_select()
        self.show_result()

    def get_browser(self):

        s=Service(ChromeDriverManager().install())
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=s, options=chrome_options)
        self.driver.get(SEARCH_URL)
        self.driver.maximize_window()


    def auto_select(self):

        # click button cookie
        self.driver.find_element(By.CLASS_NAME, 'swal2-confirm').click()

        # select dropdown location1,location2
        location1= self.driver.find_element(By.ID, 'select_location01')
        Select(location1).select_by_visible_text(INPUT_LOCATION1)
        location2= self.driver.find_element(By.ID, 'select_location02')
        Select(location2).select_by_visible_text(INPUT_LOCATION2)

        # click text date
        self.driver.find_element(By.ID,'Departdate01').click()
        # click date: css_selector
        date = datetime.today() + timedelta(days=1)
        self.driver.find_element(By.CSS_SELECTOR, f'td[data-day="{date.year}年{date.month}月{date.day}日"]').click()

        # click text time
        self.driver.find_element(By.ID,'outWardTime').click()
        self.driver.find_element(By.CSS_SELECTOR, 'span[title="Pick Hour"]').click()
        self.driver.find_elements(By.CSS_SELECTOR, 'td[data-action="selectHour"]')[int(INPUT_HOUR)].click()

        # click button search
        self.driver.find_element(By.ID, 'start-search').click()


    def show_result(self):
        
        # wait
        self.driver.implicitly_wait(5) # seconds
        
        # get title
        title_date = self.driver.find_element(By.CLASS_NAME, 'trn-datetime')
        title_location = self.driver.find_element(By.CLASS_NAME, 'trn-title')
        title_from = title_location.find_element(By.CLASS_NAME, 'from')
        title_to = title_location.find_element(By.CLASS_NAME, 'to')
        print(f'{title_date.text}  {title_from.text} -> {title_to.text}')

        # get result table
        result_table = self.driver.find_elements(By.NAME, 'timeTable')        
        for r in result_table:
            time1 = r.find_elements(By.CLASS_NAME, 'font-16r')[0]
            time2 = r.find_elements(By.CLASS_NAME, 'font-16r')[1]
            span_time = r.find_element(By.CLASS_NAME, 'traffic-time')
            print(f'出發:  {time1.text} ->(行程時間: {span_time.text})-> 抵達: {time2.text}')


if __name__ == '__main__':
    h = HSR()
    h.run()
