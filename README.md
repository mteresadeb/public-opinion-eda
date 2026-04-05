# Public Opinion EDA — Institutional Trust

Exploratory data analysis of public opinion survey data on institutional trust.

This project demonstrates how to work with national survey data to produce structured, interpretable insights about how different population groups perceive and trust public and private institutions. The analysis goes beyond simple descriptive statistics and builds a reading of the social and political landscape through data.

---

## The question

How much do people trust the institutions that shape their lives?

Trust in institutions — government, judiciary, media, armed forces, religious organizations — is one of the most studied dimensions in public opinion research. It shapes political participation, social cohesion, and the legitimacy of democratic systems.

This project shows how to explore that question systematically using survey data: measuring levels, mapping variation across demographic groups, identifying patterns, and communicating findings clearly.

---

## What this project does

- Loads and inspects a national public opinion dataset on institutional trust
- Produces univariate and bivariate summaries of trust scores (1–5 scale)
- Builds an **Institutional Trust Index (ITI)** as a composite measure
- Analyzes variation by region, age group, education, and gender
- Identifies which institutions show the greatest polarization across subgroups
- Produces publication-ready visualizations: bar charts, heatmaps, box plots, diverging charts

---

## Institutions covered

| Institution | Variable |
|---|---|
| Federal Government | `trust_gov` |
| Judiciary | `trust_judiciary` |
| National Congress | `trust_congress` |
| Armed Forces | `trust_military` |
| Media / Press | `trust_media` |
| Religious Organizations | `trust_religion` |
| NGOs and Civil Society | `trust_ngo` |
| Science and Research Institutions | `trust_science` |

---

## Project structure

```
public-opinion-eda/
│
├── notebooks/
│   └── eda_walkthrough.ipynb    # Full EDA walkthrough
│
├── scripts/
│   └── eda_pipeline.py          # Reusable EDA pipeline
│
└── README.md
```

---

## How to adapt to a new project

The analysis is driven by a configurable list of trust variables:

```python
TRUST_VARS = [
    'trust_gov',
    'trust_judiciary',
    # add or remove institutions as needed
]
```

Swap in your own variable names and the pipeline runs end to end. The ITI is recalculated automatically as the mean of whatever variables are listed.

---

## Stack

- `Python 3.x`
- `Pandas` — data preparation and group-level summaries
- `Matplotlib` — all visualizations
- `NumPy` — index calculation and numerical operations

---

## Context

The methodology demonstrated here reflects the type of analysis conducted in national public opinion studies carried out across Brazil and Latin America, including multi-country longitudinal panels with probabilistic samples. All data in this repository is synthetic and generated exclusively for demonstration purposes.

---

## Author

**Teresa De Bastiani**
Senior Market Research Analyst · Florianópolis, Brazil
[LinkedIn](https://linkedin.com/in/mteresadebastiani)
