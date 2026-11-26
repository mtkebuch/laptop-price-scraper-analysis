# Laptop Data Scraping & Cleaning Pipeline

A Python pipeline that scrapes raw laptop listings from a Georgian e-commerce site, turns messy text fields into clean numeric columns, and analyzes which specifications affect price.

**Data source:** [Ultra.ge](https://ultra.ge) (publicly available listings)

## The problem

Scraped listings arrive as text that cannot be analyzed directly:

| Field | Raw value | Cleaned value |
|---|---|---|
| Price | `1,249.00ლ` | `1249` |
| RAM | `8 GB` | `8` |
| SSD | `512 GB`, `1TB` | `512`, `1024` (GB) |
| Screen size | `14"` | `14.0` |

The pipeline scrapes the listings, converts these fields to numeric columns, and saves both the raw and cleaned datasets as Excel files.

## Pipeline

1. **Scraping** (`scraping.py`): Selenium with `ThreadPoolExecutor` collects up to 50 laptops: name, current price, original price, discount status, RAM, SSD and screen size. Uses pagination, explicit waits (`WebDriverWait`) for slow pages, a delay between requests and a small number of parallel browsers, in line with the site's robots.txt. Missing attributes are handled without crashing. Output: `ultra_prices_50.xlsx` (raw).
2. **Cleaning & statistics** (`stats_analysis.py`): Removes currency symbols and thousands separators from prices, strips units from RAM and SSD, converts prices to numbers and prints descriptive statistics (mean, median, standard deviation). Output: `clean-data.xlsx`.
3. **Regression** (`regressions.py`): Converts SSD sizes from TB to GB and compares three models for predicting the original price, using in-sample R² and 5-fold cross-validated R².

## Data quality check

Dataset collected on 26 November 2026: 50 laptops, 7 columns. No missing values and no duplicate product names in this sample. 14 of 50 laptops are discounted.

## Analysis results

Target variable: original price (before discount), in GEL.

| Model | R² (in-sample) | R² (5-fold CV) |
|---|---|---|
| Linear regression (SSD) | 0.149 | -0.045 |
| Polynomial regression, degree 2 (SSD) | 0.184 | -0.217 |
| Multiple linear regression (SSD, RAM, screen size) | **0.251** | **0.004** |

**Findings (multiple regression, fitted on all 50 laptops):**
- RAM has the strongest effect: +1 GB of RAM is associated with roughly +39.6 GEL.
- +1 GB of SSD is associated with roughly +0.70 GEL.
- Screen size has a negative coefficient (-44.5), which is not plausible as a real effect. The features are only weakly correlated (|r| ≤ 0.36), so this is more likely noise from a small sample and omitted variables such as brand and CPU.

**Limitations:** Cross-validated R² is close to zero or negative, so these models do not generalize to unseen laptops, and the polynomial model overfits the most. The sample is narrow: 42 of 50 laptops have a 512 GB SSD and RAM takes only three values (8, 12, 16 GB). Brand, CPU, GPU and discounts are not included and probably explain much of the price variation.

## Planned improvements

- Extract brand, CPU and OS from product names with regular expressions into separate columns
- Scrape the full catalog instead of 50 listings
- Move all cleaning steps into a single `cleaning.py` with validation checks
- Re-run the regression with the new features and compare cross-validated R²

## How to run

Requires Python 3 and Google Chrome.

```bash
pip install -r requirements.txt
python scraping.py
python stats_analysis.py
python regressions.py
```

Run the scripts in this order: each one uses the output of the previous step. Sample data files (`ultra_prices_50.xlsx`, `clean-data.xlsx`) are included in the repository. Prices change over time, so a fresh run may produce different numbers.

## Tech stack

Python, Selenium, pandas, scikit-learn, openpyxl