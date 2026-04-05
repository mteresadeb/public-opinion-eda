import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ─────────────────────────────────────────
# CONFIGURATION
# Adapt these variables to your project
# ─────────────────────────────────────────

INPUT_FILE = Path('./data/survey_data.csv')
OUTPUT_DIR = Path('./output')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Trust variables (expected scale: 1-5)
TRUST_VARS = [
    'trust_gov',
    'trust_judiciary',
    'trust_congress',
    'trust_military',
    'trust_media',
    'trust_religion',
    'trust_ngo',
    'trust_science',
]

INSTITUTION_LABELS = {
    'trust_gov':       'Federal Government',
    'trust_judiciary': 'Judiciary',
    'trust_congress':  'National Congress',
    'trust_military':  'Armed Forces',
    'trust_media':     'Media / Press',
    'trust_religion':  'Religious Orgs',
    'trust_ngo':       'NGOs / Civil Society',
    'trust_science':   'Science Institutions',
}

# Demographic grouping variable for subgroup comparisons
GROUP_VAR = 'region'

PALETTE = {
    'main':   '#2E86AB',
    'accent': '#E24B4A',
    'mid':    '#F18F01',
    'soft':   '#B0C4DE',
}


# ─────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────

def load_data(path):
    df = pd.read_csv(path, low_memory=False)
    missing = [v for v in TRUST_VARS if v not in df.columns]
    if missing:
        raise ValueError(f'Missing columns: {missing}')
    print(f'Data loaded: {df.shape[0]} rows, {df.shape[1]} columns')
    return df


# ─────────────────────────────────────────
# DATA QUALITY
# ─────────────────────────────────────────

def check_quality(df):
    print('=== Missing values ===')
    print(df[TRUST_VARS].isnull().sum())
    print('\n=== Value ranges (expected 1-5) ===')
    for var in TRUST_VARS:
        mn, mx = df[var].min(), df[var].max()
        flag = 'OK' if mn >= 1 and mx <= 5 else 'OUT OF RANGE'
        print(f'  {var}: min={mn}, max={mx} [{flag}]')


# ─────────────────────────────────────────
# TRUST INDEX
# ─────────────────────────────────────────

def build_index(df):
    df = df.copy()
    df['iti'] = df[TRUST_VARS].mean(axis=1).round(3)
    print(f'\nITI built. National mean: {df["iti"].mean():.3f}')
    return df


# ─────────────────────────────────────────
# RANKING
# ─────────────────────────────────────────

def plot_ranking(df):
    means = df[TRUST_VARS].mean().rename(INSTITUTION_LABELS).sort_values()
    colors = [PALETTE['accent'] if v < 2.5 else PALETTE['mid'] if v < 3.5 else PALETTE['main']
              for v in means.values]

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(means.index, means.values, color=colors, edgecolor='white', height=0.6)
    ax.axvline(3.0, color='grey', linewidth=1, linestyle='--', alpha=0.6, label='Neutral (3.0)')

    for bar, val in zip(bars, means.values):
        ax.text(val + 0.03, bar.get_y() + bar.get_height() / 2,
                f'{val:.2f}', va='center', fontsize=9)

    ax.set_xlim(1, 5.3)
    ax.set_xlabel('Mean trust score (1-5)')
    ax.set_title('Institutional trust ranking', fontsize=12)
    ax.legend(fontsize=9)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'ranking.png', dpi=150, bbox_inches='tight')
    plt.show()

    print('\nRanking:')
    for inst, score in means.sort_values(ascending=False).items():
        print(f'  {inst:<28} {score:.3f}')


# ─────────────────────────────────────────
# POLARIZATION
# ─────────────────────────────────────────

def plot_polarization(df):
    polarization = df[TRUST_VARS].std().rename(INSTITUTION_LABELS).sort_values(ascending=False)
    colors_pol = [PALETTE['accent'] if v > polarization.median() else PALETTE['main']
                  for v in polarization.values]

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(polarization.index, polarization.values,
                   color=colors_pol, edgecolor='white', height=0.6)
    ax.axvline(polarization.median(), color='grey', linewidth=1.2, linestyle='--',
               label=f'Median std: {polarization.median():.3f}')

    for bar, val in zip(bars, polarization.values):
        ax.text(val + 0.005, bar.get_y() + bar.get_height() / 2,
                f'{val:.3f}', va='center', fontsize=9)

    ax.set_xlabel('Standard deviation')
    ax.set_title('Institutional trust polarization', fontsize=12)
    ax.invert_yaxis()
    ax.legend(fontsize=9)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'polarization.png', dpi=150, bbox_inches='tight')
    plt.show()


# ─────────────────────────────────────────
# SUBGROUP HEATMAP
# ─────────────────────────────────────────

def plot_heatmap(df, group_var=GROUP_VAR):
    heatmap_data = df.groupby(group_var)[TRUST_VARS].mean().round(2)
    heatmap_data.columns = [INSTITUTION_LABELS[v] for v in TRUST_VARS]

    fig, ax = plt.subplots(figsize=(11, max(4, len(heatmap_data) * 0.7)))
    im = ax.imshow(heatmap_data.values, cmap='Blues', aspect='auto', vmin=1, vmax=5)
    plt.colorbar(im, ax=ax, label='Mean trust score (1-5)')

    ax.set_xticks(range(len(heatmap_data.columns)))
    ax.set_xticklabels(heatmap_data.columns, rotation=25, ha='right', fontsize=9)
    ax.set_yticks(range(len(heatmap_data.index)))
    ax.set_yticklabels(heatmap_data.index, fontsize=9)

    for i in range(len(heatmap_data.index)):
        for j in range(len(heatmap_data.columns)):
            val = heatmap_data.iloc[i, j]
            text_color = 'white' if val > 3.5 else 'black'
            ax.text(j, i, f'{val:.2f}', ha='center', va='center',
                    fontsize=8, color=text_color)

    ax.set_title(f'Mean trust scores by {group_var} and institution', fontsize=12)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'heatmap.png', dpi=150, bbox_inches='tight')
    plt.show()


# ─────────────────────────────────────────
# EXPORT
# ─────────────────────────────────────────

def export_results(df):
    df.to_csv(OUTPUT_DIR / 'trust_data_with_iti.csv', index=False)

    summary = df[TRUST_VARS].agg(['mean', 'median', 'std']).round(3)
    summary.columns = [INSTITUTION_LABELS[v] for v in TRUST_VARS]
    summary.to_csv(OUTPUT_DIR / 'trust_summary.csv')

    print(f'\nResults saved to: {OUTPUT_DIR}')
    print('  trust_data_with_iti.csv -- full dataset with ITI column')
    print('  trust_summary.csv       -- descriptive statistics per institution')


# ─────────────────────────────────────────
# MAIN PIPELINE
# ─────────────────────────────────────────

def run_eda(input_file=INPUT_FILE):
    print('=== Public Opinion EDA Pipeline ===\n')

    df = load_data(input_file)
    check_quality(df)
    df = build_index(df)
    plot_ranking(df)
    plot_polarization(df)
    plot_heatmap(df)
    export_results(df)

    print('\n=== Pipeline complete ===')
    return df


if __name__ == '__main__':
    run_eda()
