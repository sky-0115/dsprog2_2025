"""
デバッグ用スクリプト: 実際のHTML構造を確認
"""

import requests
from bs4 import BeautifulSoup

url = 'https://xn--pckua2a7gp15o89zb.com/%E9%A3%B2%E9%A3%9F%E5%BA%97%E3%81%AE%E4%BB%95%E4%BA%8B-%E6%9D%B1%E4%BA%AC%E9%83%BD'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}

print("HTMLを取得中...")
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# 求人カードを取得
cards = soup.find_all('section', class_='p-result_card')
print(f'\n取得した求人カード数: {len(cards)}')

# 最初の5件の詳細を表示
for i, card in enumerate(cards[:5], 1):
    print(f'\n{"="*50}')
    print(f'求人 {i}:')
    print(f'{"="*50}')
    
    # 企業名
    company = card.find('p', class_='p-result_company')
    print(f'企業名: {company.text.strip() if company else "なし"}')
    
    # 給与情報
    pay = card.find('li', class_='p-result_pay')
    print(f'給与: {pay.text.strip() if pay else "なし"}')
    
    # 雇用形態
    employ = card.find('li', class_='p-result_employType')
    print(f'雇用形態: {employ.text.strip() if employ else "なし"}')

print(f'\n{"="*50}')
print("完了")
