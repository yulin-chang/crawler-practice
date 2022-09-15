import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


SEARCH_URL = 'https://www.dcard.tw/f/food/p/235458794'


class Dcard:
    def __init__(self):
        self.root_url = SEARCH_URL
        self.driver = None
        self.total_counts = 0
        self.data = {}
    
    def run(self):
        self.set_driver()
        self.get_browser()
        self.get_total_counts()
        self.auto_scroll()
        self.feq_floor()
        self.close_browser()


    def set_driver(self):
        s=Service(ChromeDriverManager().install())
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=s, options=chrome_options)
    

    def get_browser(self):
        self.driver.get(self.root_url)


    def get_total_counts(self):
        total_info = self.driver.find_element(By.CLASS_NAME, 'sc-41b4274a-2').text
        self.total_counts = int(total_info.split(' ')[1])


    def auto_scroll(self):
        
        #初始網頁顯示1~50則留言 
        self.get_floor()

        scroll_height = 2000
        last_floor = 0
        pre_floor = 0
        cou = 0
        
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:

            # 滾動網頁, 但網頁固定只顯示10多筆留言, 所以無法一次將網頁滾動到底    
            if cou == 0:
                self.driver.execute_script(f"window.scrollTo(0, {last_height});")
                cou =1
            else:
                self.driver.execute_script(f"window.scrollTo(0, window.scrollY + {scroll_height});")

            time.sleep(3)

            last_floor = self.get_floor()

            if last_floor == self.total_counts:
                break

            # 避免迴圈
            if last_floor == pre_floor:
                scroll_height = 2500
            else:
                scroll_height = 2000
            
            pre_floor = last_floor     


    def get_floor(self):

        last_floor = 0
        comment = self.driver.find_elements(By.ID, 'comment')[0]
        
        try:
            groups = comment.find_elements(By.CLASS_NAME, 'sc-5c323813-0')

            for group in groups:
                try:
                    key = group.find_element(By.CLASS_NAME, 'sc-3651682-1').text
                    floor = group.find_element(By.CLASS_NAME, 'sc-5ebd82a8-3').text
                    # print(key, floor)
                    
                    if not any(floor in ls for ls in self.data.values()):
                        if key not in self.data:
                            self.data[key] = [floor]
                        else:
                            self.data[key].append(floor)

                        last_floor = int(floor.split('B')[1])

                except (AttributeError, NoSuchElementException, StaleElementReferenceException):
                    # 留言已被刪除
                    continue  

        except (AttributeError, NoSuchElementException, StaleElementReferenceException):
            # 留言已被刪除
            pass  

        return last_floor 


    def feq_floor(self):
        
        # print(self.data)

        freq = {}
        for key, value in self.data.items():
            freq[key] = len(value)  

        result = sorted(freq.items(), key=lambda x:x[1], reverse=True)
        
        print('該篇學校別(帳號別)的留言數排行')
        print(result)
        print('==============')
        print('總留言數:', self.total_counts)
        print('取得留言數: ', sum([r[1] for r in result]))
        

    def close_browser(self):
        self.driver.quit()
        print('quit browser!')

if __name__ == '__main__':
    d = Dcard()
    d.run()


