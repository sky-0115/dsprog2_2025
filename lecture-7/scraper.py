import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from urllib.parse import urljoin
import json

# 定数
BASE_URL = "https://xn--pckua2a7gp15o89zb.com"
# 東京都のバイト求人に絞る
SEARCH_URL = f"{BASE_URL}/%E3%83%90%E3%82%A4%E3%83%88%E3%81%AE%E4%BB%95%E4%BA%8B-%E6%9D%B1%E4%BA%AC%E9%83%BD"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
DELAY_SECONDS = 2  # リクエスト間隔（秒）

# チェーン店を示すキーワード
CHAIN_KEYWORDS = [
    "株式会社", "有限会社", "合同会社", "チェーン", "グループ",
    "ホールディングス", "HD", "Inc", "Co.,Ltd", "Corporation"
]

# 個人店を示すキーワード
INDIVIDUAL_KEYWORDS = [
    "個人", "オーナー", "自営", "家族経営"
]


def extract_hourly_wage(text):
    """
    給与テキストから時給を抽出
    例: "時給1,200円～1,500円" -> (1200, 1500)
    """
    if not text or "時給" not in text:
        return None, None
    
    # 時給のパターンを抽出
    # パターン1: 時給1,200円～1,500円
    pattern1 = r'時給([\d,]+)円(?:～|~|-)([\d,]+)円'
    match1 = re.search(pattern1, text)
    if match1:
        min_wage = int(match1.group(1).replace(',', ''))
        max_wage = int(match1.group(2).replace(',', ''))
        return min_wage, max_wage
    
    # パターン2: 時給1,200円以上
    pattern2 = r'時給([\d,]+)円以上'
    match2 = re.search(pattern2, text)
    if match2:
        wage = int(match2.group(1).replace(',', ''))
        return wage, None
    
    # パターン3: 時給1,200円
    pattern3 = r'時給([\d,]+)円'
    match3 = re.search(pattern3, text)
    if match3:
        wage = int(match3.group(1).replace(',', ''))
        return wage, wage
    
    return None, None


def classify_store_type(company_name):
    """
    企業名からチェーン店か個人店かを分類
    """
    if not company_name:
        return "不明"
    
    # チェーン店のキーワードチェック
    for keyword in CHAIN_KEYWORDS:
        if keyword in company_name:
            return "チェーン店"
    
    # 個人店のキーワードチェック
    for keyword in INDIVIDUAL_KEYWORDS:
        if keyword in company_name:
            return "個人店"
    
    # 企業名が短い場合は個人店の可能性が高い
    if len(company_name) <= 10 and "株式会社" not in company_name:
        return "個人店（推定）"
    
    return "不明"


def scrape_job_listing(url, max_pages=5):
    """
    求人一覧ページをスクレイピング
    """
    all_jobs = []
    headers = {"User-Agent": USER_AGENT}
    
    for page in range(1, max_pages + 1):
        print(f"ページ {page}/{max_pages} を取得中...")
        
        # 最初のページのみ取得（ページネーション構造が不明なため）
        page_url = url
        
        try:
            response = requests.get(page_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 求人カードを取得
            job_cards = soup.find_all('section', class_='p-result_card')
            
            if not job_cards:
                print(f"ページ {page} に求人が見つかりませんでした。終了します。")
                break
            
            print(f"  {len(job_cards)}件の求人を発見")
            
            for card in job_cards:
                job_data = {}
                
                # 企業名
                company_elem = card.find('p', class_='p-result_company')
                job_data['company_name'] = company_elem.text.strip() if company_elem else None
                
                # 求人タイトル
                title_elem = card.find('span', class_='p-result_name')
                job_data['title'] = title_elem.text.strip() if title_elem else None
                
                # 給与情報
                pay_elem = card.find('li', class_='p-result_pay')
                if pay_elem:
                    pay_text = pay_elem.text.strip()
                    job_data['pay_text'] = pay_text
                    min_wage, max_wage = extract_hourly_wage(pay_text)
                    job_data['hourly_wage_min'] = min_wage
                    job_data['hourly_wage_max'] = max_wage
                else:
                    job_data['pay_text'] = None
                    job_data['hourly_wage_min'] = None
                    job_data['hourly_wage_max'] = None
                
                # 雇用形態
                employ_elem = card.find('li', class_='p-result_employType')
                job_data['employment_type'] = employ_elem.text.strip() if employ_elem else None
                
                # 店舗タイプ分類
                job_data['store_type'] = classify_store_type(job_data['company_name'])
                
                # 時給データがある場合のみ追加
                if job_data['hourly_wage_min'] is not None:
                    all_jobs.append(job_data)
            
            # 1ページのみ取得して終了
            break
            
        except requests.RequestException as e:
            print(f"エラー発生: {e}")
            break
    
    return all_jobs


def save_data(jobs, filename='restaurant_jobs_tokyo.csv'):
    """
    収集したデータをCSVファイルに保存
    """
    if not jobs:
        print("保存するデータがありません。")
        return
    
    df = pd.DataFrame(jobs)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"\n{len(jobs)}件のデータを {filename} に保存しました。")
    
    # 統計情報を表示
    print("\n=== データ収集結果 ===")
    print(f"総求人数: {len(df)}")
    print(f"時給データあり: {len(df[df['hourly_wage_min'].notna()])}")
    print(f"\n店舗タイプ別:")
    print(df['store_type'].value_counts())


def main():
    """
    メイン処理
    """
    print("=== 求人ボックス 飲食店求人スクレイピング ===")
    print(f"対象: 東京都の飲食店")
    print(f"収集データ: 時給情報\n")
    
    # スクレイピング実行（1ページのみ取得）
    jobs = scrape_job_listing(SEARCH_URL, max_pages=1)
    
    # データ保存
    save_data(jobs)
    
    print("\n処理完了！")


if __name__ == "__main__":
    main()
