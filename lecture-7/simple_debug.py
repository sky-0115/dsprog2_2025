"""
簡易版スクレイパー: デバッグ用
"""

import requests
from bs4 import BeautifulSoup
import re

url = 'https://xn--pckua2a7gp15o89zb.com/%E9%A3%B2%E9%A3%9F%E5%BA%97%E3%81%AE%E4%BB%95%E4%BA%8B-%E6%9D%B1%E4%BA%AC%E9%83%BD?employType=2'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}

print("データ取得中...")
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

cards = soup.find_all('section', class_='p-result_card')
print(f'求人カード数: {len(cards)}\n')

hourly_count = 0
for i, card in enumerate(cards, 1):
    company = card.find('p', class_='p-result_company')
    pay = card.find('li', class_='p-result_pay')
    
    if pay:
        pay_text = pay.text.strip()
        print(f'{i}. {company.text.strip() if company else "不明"}: {pay_text}')
        
        if '時給' in pay_text:
            hourly_count += 1
            # 時給抽出テスト
            pattern1 = r'時給([\d,]+)円(?:～|~|-)([\d,]+)円'
            pattern2 = r'時給([\d,]+)円以上'
            pattern3 = r'時給(?:～|~)?([\d,]+)円'
            
            match1 = re.search(pattern1, pay_text)
            match2 = re.search(pattern2, pay_text)
            match3 = re.search(pattern3, pay_text)
            
            if match1:
                print(f'   -> パターン1: {match1.group(1)} ~ {match1.group(2)}')
            elif match2:
                print(f'   -> パターン2: {match2.group(1)}以上')
            elif match3:
                print(f'   -> パターン3: {match3.group(1)}')
            else:
                print(f'   -> マッチなし')

print(f'\n時給データ: {hourly_count}件 / {len(cards)}件')
