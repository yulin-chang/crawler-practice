import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta 
from pprint import pprint

ROOT_URL = 'https://www.taifex.com.tw/cht/3/futContractsDate'


def do_request(date):
    print(f'--> crawling: {date.strftime("%Y/%m/%d")} ({date.isoweekday()})')
    # post_str = 'queryType=1&goDay=&doQuery=1&dateaddcnt=&queryDate=2022%2F08%2F17&commodityId='
    post_str = f'queryDate={date.year}%2F{date.month}%2F{date.day}'

    re = requests.get(ROOT_URL + '?' + post_str)

    if re.status_code != requests.codes.ok:
        print('response status code 錯誤: ', re.status_code)
        return

    return re.text



def crawl_html(response_text):

    soup = BeautifulSoup(response_text, "html.parser")
    
    try:
        table = soup.find('table', class_="table_f")
        trs = table.find_all('tr')[3:-4]  # 排除 前三行標題與最後2類型: 期貨小計(3行), 期貨合計(1行)
    except AttributeError:
        print(f'無資料: {date.strftime("%Y/%m/%d")} ({date.strftime("%a")})')
        return
    

    result = {}
    for tr in trs:

        # 商品, 身份別
        if len(tr.find_all('th')) > 1:
            product = tr.find_all('th')[1]
            identity = product.find_next('th').text.strip()
            product = product.text.strip()

        else:
            identity = tr.find_all('th')[0].text.strip()

        values = tr.find_all('td')
        values = [int(value.text.strip().replace(',','')) for value in values]
            

        values_header = ['交易多方口數', '交易多方契約金額', '交易空方口數', '交易空方契約金額', '交易多空方淨額口數', '交易多空方淨額契約金額', 
                '未平倉多方口數', '未平倉多方契約金額', '未平倉空方口數', '未平倉空方契約金額', '未平倉多空方淨額口數', '未平倉多空方淨額契約金額']
            

        v_dir = {values_header[i]: values[i] for i in range(len(values_header))}


        if product not in result:
            result[product] = {identity : v_dir}
        else:
            result[product][identity] = v_dir
            

    print(f"臺股期貨|外資|未平倉多空方淨額口數:{result['臺股期貨']['外資']['未平倉多空方淨額口數']}")
        


if __name__ == '__main__':

    date = datetime.today() 
    date_now = date

    while True:

        response_text = do_request(date)
        if response_text:
            crawl_html(response_text)
        
        date = date - timedelta(days=1)
        if  date == date_now - timedelta(days=7):
            break


