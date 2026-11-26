# Laptop Price Scraper & Analysis

A Python project that scrapes laptop listings from an e-commerce website, cleans the data, and uses regression models to find out which specs affect price.

**Data source:** [Ultra.ge](https://ultra.ge) (publicly available listings)

## What it does

1. **Scraping** (`scraping.py`): Uses Selenium with `ThreadPoolExecutor` to scrape up to 50 laptops. Extracts name, current price, original price, discount status, RAM, SSD and screen size. Fetches listing pages via pagination (no `limit`, `sort` or `filter` parameters), uses a small delay between requests, and runs only a few parallel browsers, in line with the site's robots.txt. Uses `WebDriverWait` for slow-loading pages and handles missing attributes without crashing. Saves raw data to `ultra_prices_50.xlsx`.
2. **Cleaning & statistics** (`stats_analysis.py`): Removes currency symbols and thousands separators from prices, strips units from RAM and SSD values, and prints descriptive statistics (mean, median, standard deviation) for current and original prices. Saves the result to `clean-data.xlsx`.
3. **Regression** (`regressions.py`): Converts SSD sizes from TB to GB and compares three models for predicting the original price. Reports in-sample R² and 5-fold cross-validated R²:
   - Linear regression (SSD size)
   - Polynomial regression, degree 2 (SSD size)
   - Multiple linear regression (SSD, RAM, screen size)

## Results

Dataset: 50 laptops scraped from Ultra.ge. Target variable: original price (before discount), in GEL. Data collected on 26 November 2026.

| Model | R² (in-sample) | R² (5-fold CV) |
|---|---|---|
| Linear regression (SSD) | 0.149 | -0.045 |
| Polynomial regression, degree 2 (SSD) | 0.184 | -0.217 |
| Multiple linear regression (SSD, RAM, screen size) | **0.251** | **0.004** |

**Key findings (multiple regression, fitted on all 50 laptops):**
- RAM has the strongest effect: each additional 1 GB of RAM is associated with roughly +39.6 GEL in price.
- Each additional 1 GB of SSD is associated with roughly +0.70 GEL in price.
- Screen size has a negative coefficient (-44.5), which is not plausible as a real effect. The features are only weakly correlated with each other (|r| ≤ 0.36), so this is more likely noise from the small sample and omitted variables such as brand and CPU.

**Limitations:** In-sample R² looks modest but non-trivial (up to 0.25). Cross-validated R² is close to zero or negative, which means these models do not generalize to unseen laptops, and the polynomial model overfits the most. The sample is also narrow: 42 of 50 laptops have a 512 GB SSD, and RAM takes only three values (8, 12, 16 GB), so the coefficients rest on very few distinct data points. Brand, CPU, GPU and discounts are not included and probably explain much of the price variation. A larger and more varied sample with additional features would be needed for useful price prediction.

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