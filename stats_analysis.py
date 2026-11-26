import re
import pandas as pd

df = pd.read_excel("ultra_prices_50.xlsx")


def clean_price(value):
    """'1,249.00ლ' -> 1249"""
    text = str(value).replace(",", "").replace("ლ", "").strip()
    return int(float(text))


def to_gb(value):
    """'512 GB' -> 512, '1TB' -> 1024 (always returns GB as a number)"""
    match = re.search(r"([\d.]+)\s*(TB|GB)", str(value), flags=re.IGNORECASE)
    if not match:
        return None  # missing or unexpected format
    number = float(match.group(1))
    if match.group(2).upper() == "TB":
        number *= 1024
    return int(number)


df["Current Price"] = df["Current Price"].apply(clean_price)
df["Original Price"] = df["Original Price"].apply(clean_price)
df["RAM"] = df["RAM"].apply(to_gb)   # RAM is stored in GB, so the same helper works
df["SSD"] = df["SSD"].apply(to_gb)   # all SSD sizes in GB (1TB -> 1024)

# --- Data quality checks ---
print("Rows:", len(df))
print("Missing values per column:")
print(df.isna().sum().to_string())
print("Duplicate product names:", df["Product Name"].duplicated().sum())

for label in ["Current Price", "Original Price"]:
    print(f"\n{label} Statistics")
    print("Mean:", df[label].mean())
    print("Standard Deviation:", df[label].std())
    print("Median:", df[label].median())

df.to_excel("clean-data.xlsx", index=False)
print("\nCleaned data saved as: clean-data.xlsx")