import requests
from bs4 import BeautifulSoup

ROOT_URL = 'https://tw.stock.yahoo.com/quote/'

def do_request(num):
    re = requests.get(ROOT_URL + str(num) + '.TW')

    if re.status_code != requests.codes.ok:
        print('response status code 錯誤: ', re.status_code)
        exit(1)
    return re.text


def crawl_html(response_text):
    yahoo = BeautifulSoup(response_text, 'html.parser')
    
    #台股名稱, 代號
    main_info = yahoo.select('#main-0-QuoteHeader-Proxy')[0]
    title = main_info.find('h1')
    number = title.find_next('span')
    print(f'{title.text}-{number.text}')
    
    # 狀態, 最後時間
    status_date = main_info.find_all('span', class_='C(#6e7780) Fz(12px) Fw(b)')[0]
    print(f'{status_date.text}')


    # 股價
    ul = yahoo.find_all('ul', class_='D(f) Fld(c) Flw(w) H(192px) Mx(-16px)')[0]
    
    # 成交
    li_0 = ul.find('li')  
    name_0 = li_0.find('span')
    value_0 = name_0.find_next('span')  
    print(f'{name_0.text}: {value_0.text}')

    # 最高
    li_1 = ul.find_all('li')[2]  
    name_1 = li_1.find('span')  
    value_1 = name_1.find_next('span')  
    print(f'{name_1.text}: {value_1.text}')

    # 最低
    li_2 = li_1.find_next('li')  
    name_2 = li_2.find('span')  
    value_2 = name_2.find_next('span') 
    print(f'{name_2.text}: {value_2.text}')



if __name__ == '__main__':

    num = input("輸入台股代號(預設2330):")  # EX: 2330
    if num.isnumeric():
        crawl_html(do_request(num))
    else:
        if num == '':
            crawl_html(do_request('2330'))
        else:
            print('輸入錯誤!')
    

    

        