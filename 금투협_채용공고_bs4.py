import requests
from bs4 import BeautifulSoup
import logging
import pandas as pd

url = "https://www.kofia.or.kr/brd/m_96/"
list_path = "list.do?"

def scrape_job(url, page_nums = 11):

    scraped_table = []
    
    for page_num in range(1, page_nums):
        
        params = {
            'page' : page_num
            }
        res = requests.get(url + list_path, params = params)

        if res.status_code != 200:
            print('connection not established')
            raise ConnectionError

        else:
            soup = BeautifulSoup(res.content, 'html.parser')
            rows = soup.select('div#contentArea2 tbody tr')

            try:
                for row in rows:
                    number = row.select_one('td.first.num').get_text()
                    title = row.select_one('td.left.new').get_text()
                    content_link = row.select_one('td.left.new a').attrs['href']
                    upload_date = row.select_one('td.num')
                    res = [number, title, url + content_link, upload_date]

                    scraped_table.append(res)

            except AttributeError:
                continue

    return scraped_table

if __name__ == "__main__":

    result = scrape_job(url, page_nums = 3)
    df = pd.DataFrame(result, columns = ['number', 'title', 'link', 'updated_date']).set_index('number')
    print(df)


