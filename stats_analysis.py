import pandas as pd

df = pd.read_excel("ultra_prices_50.xlsx")

df["Current Price"] = df["Current Price"].astype(str) \
    .str.replace(",", "") \
    .str.replace("ლ", "") \
    .str.strip()
df["Current Price"] = df["Current Price"].astype(float).astype(int)

df["Original Price"] = df["Original Price"].astype(str) \
    .str.replace(",", "") \
    .str.replace("ლ", "") \
    .str.strip()
df["Original Price"] = df["Original Price"].astype(float).astype(int)

df["RAM"] = df["RAM"].astype(str).str.replace("GB", "").str.strip()
df["SSD"] = df["SSD"].astype(str).str.replace("GB", "").str.strip()

mean_current = df["Current Price"].mean()
std_current = df["Current Price"].std()
median_current = df["Current Price"].median()

print("Current Price Statistics")
print("Mean:", mean_current)
print("Standard Deviation:", std_current)
print("Median:", median_current)

mean_original = df["Original Price"].mean()
std_original = df["Original Price"].std()
median_original = df["Original Price"].median()

print("\nOriginal Price Statistics")
print("Mean:", mean_original)
print("Standard Deviation:", std_original)
print("Median:", median_original)

df.to_excel("clean-data.xlsx", index=False)
print("\nCleaned data saved as: clean-data.xlsx")
