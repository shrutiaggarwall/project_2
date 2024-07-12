import requests
import pandas as pd
import json
from datetime import date, timedelta

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': '_ga=GA1.1.1705804826.1720472457; JSESSIONID=83F19B643A6B0C34B93866FD2BA16478; _ga_2RYZG7Y4NC=GS1.1.1720498263.2.1.1720498263.0.0.0; __gads=ID=2b8daa3ce303322a:T=1720472456:RT=1720498262:S=ALNI_MYmwDtajHvuPvJjaIQ1HNnSfvhKXw; __eoi=ID=0cd3f4ccce8ec1c8:T=1720472456:RT=1720498262:S=AA-AfjajcEPGB19B02Dpf_37TQuA; FCNEC=%5B%5B%22AKsRol9AoevajS8vaeYqF7olKzI5nJkKQCGdukdlqcsD08ngcP1Q3ulckxufv5zFwhUN3XHRhJt-mPegnWxfHbBHRyXz5wYqvfnsTN5Rn_AWi_P4mQQzzWG7cU0iL5EOu03_dW1dvIiPgYhCimrhJU3l8c8eaOemKQ%3D%3D%22%5D%5D',
    'Host': 'vegetablemarketprice.com',
    'Referer': 'https://vegetablemarketprice.com/market/delhi/today',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

start_date = date(2024, 5, 1)
end_date = date(2024, 6, 30)
date_ = start_date

data = []

while date_ <= end_date:
    print(f"Scraping data for {date_}...")
    url = f'https://vegetablemarketprice.com/api/dataapi/market/delhi/daywisedata?date={date_}'
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        js_data = response.json()
        
        for vegetable in js_data['data']:
            dict_veg = {}
            dict_veg['date'] = date_
            dict_veg['state'] = 'New Delhi'
            dict_veg['name'] = vegetable['vegetablename']
            dict_veg['wholesalePrice'] = vegetable['price']
            dict_veg['retailPrice'] = vegetable['retailprice']
            dict_veg['shoppingmallPrice'] = vegetable['shopingmallprice']
            dict_veg['units'] = vegetable['units']
            dict_veg['image'] = vegetable['table']['table_image_url']
            
            data.append(dict_veg)
    
    else:
        print(f"Failed to retrieve data for {date_}. Status code: {response.status_code}")
    
    date_ += timedelta(days=1)

df = pd.DataFrame(data)

df.to_csv('vegetable_prices_delhi.csv', index=False)

print("Data scraping and saving completed!")