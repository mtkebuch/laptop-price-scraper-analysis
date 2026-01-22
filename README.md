Laptop Price Scraping, Cleaning and Regression Analysis

This project automates the process of collecting laptop data from an e-commerce website, cleaning the extracted dataset, performing statistical analysis, and building multiple regression models to understand the factors affecting laptop prices.

Project Structure

1. Web Scraping (scraping.py)

Uses Selenium and concurrent threading to scrape up to 50 laptop items.
Extracts product name, current price, original price, discount status, RAM, SSD, and screen size.
Handles slow-loading pages with WebDriverWait.
Saves the scraped dataset to ultra_prices_50.xlsx.

2. Data Cleaning & Statistics (stats_analysis.py)

Cleans numeric values (prices, RAM, SSD).
Converts storage units (GB/TB).
Generates descriptive statistics such as mean, median, and standard deviation.
Saves the cleaned dataset as clean-data.xlsx.

3. Regression Models (regression.py)

Builds and evaluates several models to estimate laptop prices:
Linear Regression using SSD size
Multiple Linear Regression using SSD, RAM, and Screen Size
Polynomial Regression (degree 2) for capturing non-linear relationships
Compares model performance using R² scores and identifies the best-performing model.

Features

Automated parallel scraping using ThreadPoolExecutor
Robust error handling for missing product attributes
Clean preprocessing pipeline for numerical fields
Statistical summary of the dataset
Comparison between linear, multiple, and polynomial regression models
Well-structured code suitable for portfolio presentation

Purpose

This project demonstrates practical skills in web automation, data engineering, and applied machine learning. It is designed as a complete workflow—from data collection to predictive modeling—showcasing both backend scraping logic and analytical capabilities.
