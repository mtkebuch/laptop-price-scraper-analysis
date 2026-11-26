import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import KFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

# --- Load data ---
df = pd.read_excel("clean-data.xlsx")

# Convert SSD to GB (TB values are multiplied by 1024)
df["SSD_GB"] = df["SSD"].astype(str).str.replace("TB", "").astype(float)
df.loc[df["SSD"].astype(str).str.contains("TB", na=False), "SSD_GB"] *= 1024

y = df["Original Price"]

# --- Model 1: Linear regression (SSD only) ---
X_linear = df[["SSD_GB"]]

linear_model = LinearRegression()
linear_model.fit(X_linear, y)
r2_linear = r2_score(y, linear_model.predict(X_linear))

print("\n--- Linear Regression (SSD only) ---")
print("R²:", r2_linear)
print("Price increase per 1GB SSD:", linear_model.coef_[0])
print("Intercept:", linear_model.intercept_)

# --- Model 2: Polynomial regression (SSD only, degree 2) ---
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X_linear)

poly_model = LinearRegression()
poly_model.fit(X_poly, y)
r2_poly = r2_score(y, poly_model.predict(X_poly))

print("\n--- Polynomial Regression (SSD only, degree=2) ---")
print("R²:", r2_poly)
print("Coefficient SSD_GB:", poly_model.coef_[0])
print("Coefficient SSD_GB^2:", poly_model.coef_[1])
print("Intercept:", poly_model.intercept_)

# --- Model 3: Multiple linear regression ---
X_multi = df[["SSD_GB", "RAM", "Screen Size"]]

multi_model = LinearRegression()
multi_model.fit(X_multi, y)
r2_multi = r2_score(y, multi_model.predict(X_multi))

print("\n--- Multiple Linear Regression ---")
print("R²:", r2_multi)
print("SSD coefficient:", multi_model.coef_[0])
print("RAM coefficient:", multi_model.coef_[1])
print("Screen Size coefficient:", multi_model.coef_[2])
print("Intercept:", multi_model.intercept_)

# --- Model comparison (in-sample) ---
print("\n--- Model Comparison (in-sample R²) ---")
print("Linear Regression:", r2_linear)
print("Polynomial Regression:", r2_poly)
print("Multiple Regression:", r2_multi)

best_model = max(
    (r2_linear, "Linear Regression"),
    (r2_poly, "Polynomial Regression"),
    (r2_multi, "Multiple Regression"),
)

print("\nBest Model (in-sample):", best_model[1], "with R² =", best_model[0])

# --- Cross-validation (5-fold) ---
cv = KFold(n_splits=5, shuffle=True, random_state=42)
models = {
    "Linear Regression": (LinearRegression(), X_linear),
    "Polynomial Regression": (
        make_pipeline(PolynomialFeatures(degree=2, include_bias=False), LinearRegression()),
        X_linear,
    ),
    "Multiple Regression": (LinearRegression(), X_multi),
}

print("\n--- Cross-validated R² (5-fold) ---")
for name, (model, features) in models.items():
    scores = cross_val_score(model, features, y, cv=cv, scoring="r2")
    print(f"{name}: {scores.mean():.3f}")