"""
複数ページから収集した求人データの統計分析
チェーン店と個人店の時給範囲を比較して仮説を検証
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# 日本語フォント設定
plt.rcParams['font.sans-serif'] = ['Hiragino Sans', 'Yu Gothic', 'Meiryo', 'Takao', 'IPAexGothic', 'IPAPGothic']
plt.rcParams['axes.unicode_minus'] = False


def load_data(filename='restaurant_jobs_tokyo_multipage.csv'):
    """
    CSVファイルからデータを読み込み
    """
    try:
        df = pd.read_csv(filename, encoding='utf-8-sig')
        print(f"✓ データ読み込み完了: {len(df)}件\n")
        return df
    except FileNotFoundError:
        print(f"エラー: {filename} が見つかりません。")
        print("先に scraper_multipage.py を実行してデータを収集してください。")
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
    print("=" * 70)
    print("=== チェーン店 vs 個人店 統計分析 ===")
    print("=" * 70)
    
    # チェーン店と個人店のデータを抽出
    chain_stores = df[df['store_type'] == 'チェーン店'].copy()
    individual_stores = df[df['store_type'].isin(['個人店', '個人店（推定）'])].copy()
    
    print(f"\n【サンプルサイズ】")
    print(f"  チェーン店:  {len(chain_stores):3d}件")
    print(f"  個人店:     {len(individual_stores):3d}件")
    
    if len(chain_stores) == 0 or len(individual_stores) == 0:
        print("\nデータが不足しているため、分析を中止します。")
        return
    
    # 1. 時給範囲の統計
    print(f"\n【時給範囲（円）の統計】")
    print(f"\n  チェーン店:")
    print(f"    平均:     {chain_stores['wage_range'].mean():7.1f}円")
    print(f"    中央値:   {chain_stores['wage_range'].median():7.1f}円")
    print(f"    標準偏差: {chain_stores['wage_range'].std():7.1f}円")
    print(f"    最小値:   {chain_stores['wage_range'].min():7.1f}円")
    print(f"    最大値:   {chain_stores['wage_range'].max():7.1f}円")
    
    print(f"\n  個人店:")
    print(f"    平均:     {individual_stores['wage_range'].mean():7.1f}円")
    print(f"    中央値:   {individual_stores['wage_range'].median():7.1f}円")
    print(f"    標準偏差: {individual_stores['wage_range'].std():7.1f}円")
    print(f"    最小値:   {individual_stores['wage_range'].min():7.1f}円")
    print(f"    最大値:   {individual_stores['wage_range'].max():7.1f}円")
    
    # 2. 最低時給の統計
    print(f"\n【最低時給（円）の統計】")
    print(f"\n  チェーン店:")
    print(f"    平均:     {chain_stores['hourly_wage_min'].mean():7.1f}円")
    print(f"    中央値:   {chain_stores['hourly_wage_min'].median():7.1f}円")
    print(f"    標準偏差: {chain_stores['hourly_wage_min'].std():7.1f}円")
    
    print(f"\n  個人店:")
    print(f"    平均:     {individual_stores['hourly_wage_min'].mean():7.1f}円")
    print(f"    中央値:   {individual_stores['hourly_wage_min'].median():7.1f}円")
    print(f"    標準偏差: {individual_stores['hourly_wage_min'].std():7.1f}円")
    
    # 3. 最高時給の統計
    print(f"\n【最高時給（円）の統計】")
    print(f"\n  チェーン店:")
    print(f"    平均:     {chain_stores['hourly_wage_max'].mean():7.1f}円")
    print(f"    中央値:   {chain_stores['hourly_wage_max'].median():7.1f}円")
    print(f"    標準偏差: {chain_stores['hourly_wage_max'].std():7.1f}円")
    
    print(f"\n  個人店:")
    print(f"    平均:     {individual_stores['hourly_wage_max'].mean():7.1f}円")
    print(f"    中央値:   {individual_stores['hourly_wage_max'].median():7.1f}円")
    print(f"    標準偏差: {individual_stores['hourly_wage_max'].std():7.1f}円")
    
    # 4. 統計的検定
    print(f"\n" + "=" * 70)
    print("=== 統計的仮説検定（t検定） ===")
    print("=" * 70)
    
    # 時給範囲の差の検定
    t_stat_range, p_value_range = stats.ttest_ind(
        individual_stores['wage_range'].dropna(),
        chain_stores['wage_range'].dropna()
    )
    print(f"\n【時給範囲の比較】")
    print(f"  t値:        {t_stat_range:7.4f}")
    print(f"  p値:        {p_value_range:7.4f}")
    print(f"  有意水準:   α = 0.05")
    
    if p_value_range < 0.05:
        print(f"  結論: ✓ 有意差あり")
        diff = individual_stores['wage_range'].mean() - chain_stores['wage_range'].mean()
        if diff > 0:
            print(f"  → 個人店の時給範囲が【有意に広い】傾向を確認しました！")
            print(f"  → 差分: {diff:.1f}円（個人店が高い）")
        else:
            print(f"  → チェーン店の時給範囲が【有意に広い】傾向を確認しました。")
            print(f"  → 差分: {-diff:.1f}円（チェーン店が高い）")
    else:
        print(f"  結論: ✗ 有意差なし（p ≥ 0.05）")
        print(f"  → 時給範囲に有意な差異は見られません")
    
    # 最低時給の差の検定
    t_stat_min, p_value_min = stats.ttest_ind(
        individual_stores['hourly_wage_min'].dropna(),
        chain_stores['hourly_wage_min'].dropna()
    )
    print(f"\n【最低時給の比較】")
    print(f"  t値:        {t_stat_min:7.4f}")
    print(f"  p値:        {p_value_min:7.4f}")
    if p_value_min < 0.05:
        print(f"  結論: ✓ 有意差あり")
    else:
        print(f"  結論: ✗ 有意差なし（p ≥ 0.05）")
    
    # 最高時給の差の検定
    t_stat_max, p_value_max = stats.ttest_ind(
        individual_stores['hourly_wage_max'].dropna(),
        chain_stores['hourly_wage_max'].dropna()
    )
    print(f"\n【最高時給の比較】")
    print(f"  t値:        {t_stat_max:7.4f}")
    print(f"  p値:        {p_value_max:7.4f}")
    if p_value_max < 0.05:
        print(f"  結論: ✓ 有意差あり")
    else:
        print(f"  結論: ✗ 有意差なし（p ≥ 0.05）")
    
    return chain_stores, individual_stores


def visualize_data(df, chain_stores, individual_stores):
    """
    データの可視化
    """
    print(f"\n" + "=" * 70)
    print("=== グラフ生成中 ===")
    print("=" * 70)
    
    # 図の作成（さらに大きめのサイズ）
    fig = plt.figure(figsize=(20, 15))
    gs = fig.add_gridspec(3, 2, hspace=0.35, wspace=0.35)
    
    fig.suptitle('東京都 飲食店バイト求人の時給分析: チェーン店 vs 個人店\n(n=449件)', 
                 fontsize=22, fontweight='bold', y=0.995)
    
    # 1. 時給範囲の箱ひげ図（外れ値を除いたy軸範囲設定）
    ax1 = fig.add_subplot(gs[0, 0])
    data_range = [
        chain_stores['wage_range'].dropna(),
        individual_stores['wage_range'].dropna()
    ]
    bp1 = ax1.boxplot(data_range, labels=['チェーン店', '個人店'], patch_artist=True, widths=0.6)
    bp1['boxes'][0].set_facecolor('#3498db')
    bp1['boxes'][1].set_facecolor('#e74c3c')
    # y軸範囲を95パーセンタイルまでに制限
    all_range_data = pd.concat([chain_stores['wage_range'], individual_stores['wage_range']]).dropna()
    ax1.set_ylim(-50, all_range_data.quantile(0.95) * 1.1)
    ax1.set_ylabel('時給範囲（円）', fontsize=14, fontweight='bold')
    ax1.set_title('時給範囲の比較（中央値、四分位数）', fontsize=15, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    # 2. 最低時給の箱ひげ図（外れ値を除いたy軸範囲設定）
    ax2 = fig.add_subplot(gs[0, 1])
    data_min = [
        chain_stores['hourly_wage_min'].dropna(),
        individual_stores['hourly_wage_min'].dropna()
    ]
    bp2 = ax2.boxplot(data_min, labels=['チェーン店', '個人店'], patch_artist=True, widths=0.6)
    bp2['boxes'][0].set_facecolor('#3498db')
    bp2['boxes'][1].set_facecolor('#e74c3c')
    # y軸範囲を95パーセンタイルまでに制限
    all_min_data = pd.concat([chain_stores['hourly_wage_min'], individual_stores['hourly_wage_min']]).dropna()
    ax2.set_ylim(all_min_data.quantile(0.05) * 0.95, all_min_data.quantile(0.95) * 1.05)
    ax2.set_ylabel('最低時給（円）', fontsize=14, fontweight='bold')
    ax2.set_title('最低時給の比較', fontsize=15, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    
    # 3. 時給範囲のヒストグラム
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.hist(chain_stores['wage_range'].dropna(), bins=30, alpha=0.6, label='チェーン店', 
             color='#3498db', edgecolor='black', linewidth=0.5)
    ax3.hist(individual_stores['wage_range'].dropna(), bins=30, alpha=0.6, label='個人店', 
             color='#e74c3c', edgecolor='black', linewidth=0.5)
    ax3.set_xlabel('時給範囲（円）', fontsize=14, fontweight='bold')
    ax3.set_ylabel('求人数', fontsize=14, fontweight='bold')
    ax3.set_title('時給範囲の分布（ヒストグラム）', fontsize=15, fontweight='bold')
    ax3.legend(fontsize=13)
    ax3.grid(axis='y', alpha=0.3, linestyle='--')
    
    # 4. 最低時給のヒストグラム
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.hist(chain_stores['hourly_wage_min'].dropna(), bins=30, alpha=0.6, label='チェーン店', 
             color='#3498db', edgecolor='black', linewidth=0.5)
    ax4.hist(individual_stores['hourly_wage_min'].dropna(), bins=30, alpha=0.6, label='個人店', 
             color='#e74c3c', edgecolor='black', linewidth=0.5)
    ax4.set_xlabel('最低時給（円）', fontsize=14, fontweight='bold')
    ax4.set_ylabel('求人数', fontsize=14, fontweight='bold')
    ax4.set_title('最低時給の分布（ヒストグラム）', fontsize=15, fontweight='bold')
    ax4.legend(fontsize=13)
    ax4.grid(axis='y', alpha=0.3, linestyle='--')
    # x軸ラベルを回転させて見やすく
    ax4.tick_params(axis='x', labelsize=11, rotation=45)
    
    # 5. 最高時給のバイオリンプロット（外れ値を除いたy軸範囲設定）
    ax5 = fig.add_subplot(gs[2, 0])
    plot_data = [
        chain_stores['hourly_wage_max'].dropna(),
        individual_stores['hourly_wage_max'].dropna()
    ]
    parts = ax5.violinplot(plot_data, positions=[1, 2], showmeans=True, showmedians=True)
    ax5.set_xticks([1, 2])
    ax5.set_xticklabels(['チェーン店', '個人店'], fontsize=13)
    # y軸範囲を95パーセンタイルまでに制限
    all_max_data = pd.concat([chain_stores['hourly_wage_max'], individual_stores['hourly_wage_max']]).dropna()
    ax5.set_ylim(all_max_data.quantile(0.05) * 0.95, all_max_data.quantile(0.95) * 1.05)
    ax5.set_ylabel('最高時給（円）', fontsize=14, fontweight='bold')
    ax5.set_title('最高時給の分布（バイオリンプロット）', fontsize=15, fontweight='bold')
    ax5.grid(axis='y', alpha=0.3, linestyle='--')
    
    # 6. 統計サマリーテーブル
    ax6 = fig.add_subplot(gs[2, 1])
    ax6.axis('off')
    
    summary_data = [
        ['指標', 'チェーン店', '個人店'],
        ['', '', ''],
        ['時給範囲（円）', '', ''],
        ['  平均', f'{chain_stores["wage_range"].mean():.0f}', f'{individual_stores["wage_range"].mean():.0f}'],
        ['  中央値', f'{chain_stores["wage_range"].median():.0f}', f'{individual_stores["wage_range"].median():.0f}'],
        ['  標準偏差', f'{chain_stores["wage_range"].std():.0f}', f'{individual_stores["wage_range"].std():.0f}'],
        ['', '', ''],
        ['最低時給（円）', '', ''],
        ['  平均', f'{chain_stores["hourly_wage_min"].mean():.0f}', f'{individual_stores["hourly_wage_min"].mean():.0f}'],
        ['  中央値', f'{chain_stores["hourly_wage_min"].median():.0f}', f'{individual_stores["hourly_wage_min"].median():.0f}'],
        ['', '', ''],
        ['最高時給（円）', '', ''],
        ['  平均', f'{chain_stores["hourly_wage_max"].mean():.0f}', f'{individual_stores["hourly_wage_max"].mean():.0f}'],
        ['  中央値', f'{chain_stores["hourly_wage_max"].median():.0f}', f'{individual_stores["hourly_wage_max"].median():.0f}'],
    ]
    
    table = ax6.table(cellText=summary_data, cellLoc='center', loc='center',
                     colWidths=[0.35, 0.3, 0.3])
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 2.2)
    
    # ヘッダー行のスタイル
    for i in range(3):
        table[(0, i)].set_facecolor('#34495e')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # 行のスタイル分け
    for i in range(1, len(summary_data)):
        if summary_data[i][0] == '':
            continue
        if summary_data[i][0].strip() and not summary_data[i][0].startswith('  '):
            for j in range(3):
                table[(i, j)].set_facecolor('#ecf0f1')
                table[(i, j)].set_text_props(weight='bold')
        else:
            for j in range(3):
                table[(i, j)].set_facecolor('#f8f9fa')
    
    plt.savefig('wage_analysis_multipage.png', dpi=300, bbox_inches='tight')
    print("✓ グラフを wage_analysis_multipage.png に保存しました。")


def main():
    """
    メイン処理
    """
    print("\n" + "=" * 70)
    print("=== 求人データ分析（複数ページ版） ===")
    print("=" * 70 + "\n")
    
    # データ読み込み
    df = load_data()
    if df is None:
        return
    
    # 時給範囲を計算
    df = calculate_wage_range(df)
    
    # 統計分析
    chain_stores, individual_stores = analyze_by_store_type(df)
    
    # 可視化
    visualize_data(df, chain_stores, individual_stores)
    
    print("\n" + "=" * 70)
    print("✓ 分析完了！")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
