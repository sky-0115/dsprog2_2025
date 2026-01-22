import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# 日本語フォント設定
plt.rcParams['font.sans-serif'] = ['Hiragino Sans', 'Yu Gothic', 'Meiryo', 'Takao', 'IPAexGothic', 'IPAPGothic']
plt.rcParams['axes.unicode_minus'] = False


def load_data(filename='restaurant_jobs_tokyo.csv'):
    """
    CSVファイルからデータを読み込み
    """
    try:
        df = pd.read_csv(filename, encoding='utf-8-sig')
        print(f"データ読み込み完了: {len(df)}件")
        return df
    except FileNotFoundError:
        print(f"エラー: {filename} が見つかりません。")
        print("先に scraper.py を実行してデータを収集してください。")
        return None


def calculate_wage_range(df):
    """
    時給の範囲（最大値 - 最小値）を計算
    """
    df = df.copy()
    
    # 時給範囲を計算
    df['wage_range'] = df.apply(
        lambda row: (row['hourly_wage_max'] - row['hourly_wage_min']) 
        if pd.notna(row['hourly_wage_max']) and pd.notna(row['hourly_wage_min'])
        else 0,
        axis=1
    )
    
    return df


def analyze_by_store_type(df):
    """
    店舗タイプ別の統計分析
    """
    print("\n=== 店舗タイプ別 統計分析 ===\n")
    
    # チェーン店と個人店のデータを抽出
    chain_stores = df[df['store_type'] == 'チェーン店']
    individual_stores = df[df['store_type'].isin(['個人店', '個人店（推定）'])]
    
    print(f"チェーン店: {len(chain_stores)}件")
    print(f"個人店: {len(individual_stores)}件")
    
    if len(chain_stores) == 0 or len(individual_stores) == 0:
        print("データが不足しているため、分析を中止します。")
        return
    
    # 時給範囲の統計
    print("\n--- 時給範囲（円）の統計 ---")
    print("\nチェーン店:")
    print(chain_stores['wage_range'].describe())
    
    print("\n個人店:")
    print(individual_stores['wage_range'].describe())
    
    # 平均時給の統計
    print("\n--- 最低時給（円）の統計 ---")
    print("\nチェーン店:")
    print(chain_stores['hourly_wage_min'].describe())
    
    print("\n個人店:")
    print(individual_stores['hourly_wage_min'].describe())
    
    # t検定で有意差を確認
    print("\n--- 統計的検定 ---")
    
    # 時給範囲の差の検定
    t_stat_range, p_value_range = stats.ttest_ind(
        individual_stores['wage_range'].dropna(),
        chain_stores['wage_range'].dropna()
    )
    print(f"\n時給範囲の差の検定:")
    print(f"  t値: {t_stat_range:.4f}")
    print(f"  p値: {p_value_range:.4f}")
    if p_value_range < 0.05:
        print(f"  結果: 有意差あり（p < 0.05）")
        if individual_stores['wage_range'].mean() > chain_stores['wage_range'].mean():
            print(f"  → 個人店の時給範囲が広い傾向が確認されました！")
        else:
            print(f"  → チェーン店の時給範囲が広い傾向が確認されました。")
    else:
        print(f"  結果: 有意差なし（p >= 0.05）")
    
    # 最低時給の差の検定
    t_stat_min, p_value_min = stats.ttest_ind(
        individual_stores['hourly_wage_min'].dropna(),
        chain_stores['hourly_wage_min'].dropna()
    )
    print(f"\n最低時給の差の検定:")
    print(f"  t値: {t_stat_min:.4f}")
    print(f"  p値: {p_value_min:.4f}")
    if p_value_min < 0.05:
        print(f"  結果: 有意差あり（p < 0.05）")
    else:
        print(f"  結果: 有意差なし（p >= 0.05）")


def visualize_data(df):
    """
    データの可視化
    """
    # チェーン店と個人店のデータを抽出
    chain_stores = df[df['store_type'] == 'チェーン店']
    individual_stores = df[df['store_type'].isin(['個人店', '個人店（推定）'])]
    
    if len(chain_stores) == 0 or len(individual_stores) == 0:
        print("可視化に必要なデータが不足しています。")
        return
    
    # 図の作成
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('東京都 飲食店求人の時給分析: チェーン店 vs 個人店', fontsize=16, fontweight='bold')
    
    # 1. 時給範囲の箱ひげ図
    ax1 = axes[0, 0]
    data_range = [
        chain_stores['wage_range'].dropna(),
        individual_stores['wage_range'].dropna()
    ]
    bp1 = ax1.boxplot(data_range, labels=['チェーン店', '個人店'], patch_artist=True)
    bp1['boxes'][0].set_facecolor('lightblue')
    bp1['boxes'][1].set_facecolor('lightcoral')
    ax1.set_ylabel('時給範囲（円）', fontsize=12)
    ax1.set_title('時給範囲の比較', fontsize=13, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # 2. 最低時給の箱ひげ図
    ax2 = axes[0, 1]
    data_min = [
        chain_stores['hourly_wage_min'].dropna(),
        individual_stores['hourly_wage_min'].dropna()
    ]
    bp2 = ax2.boxplot(data_min, labels=['チェーン店', '個人店'], patch_artist=True)
    bp2['boxes'][0].set_facecolor('lightblue')
    bp2['boxes'][1].set_facecolor('lightcoral')
    ax2.set_ylabel('最低時給（円）', fontsize=12)
    ax2.set_title('最低時給の比較', fontsize=13, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    # 3. 時給範囲のヒストグラム
    ax3 = axes[1, 0]
    ax3.hist(chain_stores['wage_range'].dropna(), bins=20, alpha=0.6, label='チェーン店', color='lightblue', edgecolor='black')
    ax3.hist(individual_stores['wage_range'].dropna(), bins=20, alpha=0.6, label='個人店', color='lightcoral', edgecolor='black')
    ax3.set_xlabel('時給範囲（円）', fontsize=12)
    ax3.set_ylabel('求人数', fontsize=12)
    ax3.set_title('時給範囲の分布', fontsize=13, fontweight='bold')
    ax3.legend()
    ax3.grid(axis='y', alpha=0.3)
    
    # 4. 最低時給のヒストグラム
    ax4 = axes[1, 1]
    ax4.hist(chain_stores['hourly_wage_min'].dropna(), bins=20, alpha=0.6, label='チェーン店', color='lightblue', edgecolor='black')
    ax4.hist(individual_stores['hourly_wage_min'].dropna(), bins=20, alpha=0.6, label='個人店', color='lightcoral', edgecolor='black')
    ax4.set_xlabel('最低時給（円）', fontsize=12)
    ax4.set_ylabel('求人数', fontsize=12)
    ax4.set_title('最低時給の分布', fontsize=13, fontweight='bold')
    ax4.legend()
    ax4.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('wage_analysis.png', dpi=300, bbox_inches='tight')
    print("\nグラフを wage_analysis.png に保存しました。")
    plt.show()


def main():
    """
    メイン処理
    """
    print("=== 求人データ分析 ===")
    
    # データ読み込み
    df = load_data()
    if df is None:
        return
    
    # 時給範囲を計算
    df = calculate_wage_range(df)
    
    # 統計分析
    analyze_by_store_type(df)
    
    # 可視化
    visualize_data(df)
    
    print("\n分析完了！")


if __name__ == "__main__":
    main()
