# from selenium import webdriver
# from selectolax.parser import HTMLParser
# import json
# from urllib.parse import unquote
#
# URL = 'https://www.avito.ru/kazan/komnaty/prodam-ASgBAgICAUSQA7wQ?context=H4sIAAAAAAAA_0q0MrSqLraysFJKK8rPDUhMT1WyLrYyNLNSKk5NLErOcMsvyg3PTElPLVGyrgUEAAD__xf8iH4tAAAA&f=ASgBAgECAUSQA7wQAkX6BxV7ImZyb20iOjE2LCJ0byI6bnVsbH3GmgwXeyJmcm9tIjowLCJ0byI6MjAwMDAwMH0&s=104&p=3'
#
# driver = webdriver.Chrome()
# driver.get(URL)
#
# html = driver.execute_script("return document.documentElement.outerHTML;")
# print('HERE')
# if 'Ничего не найдено' in html:
#     print('THERE!')
#     exit(0)
#
# tree = HTMLParser(html)
# scripts = tree.css('script')
#
# json_data: dict = {}
#
# for script in scripts:
#     if 'window.__initialData__' in script.text():
#         print('HERE')
#         json_raw = unquote(script.text().split(';')[0].split('=')[1].strip().strip('"'))
#         json_data = json.loads(json_raw)
#
# print(json_data)
# print(len(json_data))

import os

# links = pd.read_csv(LINKS_FILEPATH, delimiter=',', index_col=0)
# url: str = links['url'][0]
# export_df = pd.DataFrame(columns=REALTY_COLUMNS)
#
# for page in range(1, 101):
#     print(page)
#     raw_offers = get_new_offers(url + f'&p={page}', 123456789, update_db=False)
#
#     if not raw_offers:
#         break
#     values_list = [d.values() for d in raw_offers]
#     export_df = pd.concat([export_df, pd.DataFrame(values_list, columns=REALTY_COLUMNS)])
#
# print(export_df)
# export_df.to_excel(XLSX_FILEPATH)

folder_path = os.path.join('bot', 'files')

print(os.path.exists(folder_path))

if not os.path.exists(folder_path):
    os.mkdir(folder_path)

print(os.path.exists(folder_path))
