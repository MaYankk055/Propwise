"""
India Real Estate ML Pipeline
Advanced model with city-aware features and proper evaluation
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib, json, warnings
warnings.filterwarnings('ignore')

os.makedirs('static', exist_ok=True)
os.makedirs('model', exist_ok=True)

# ── Load Data ─────────────────────────────────────────────────
df = pd.read_csv('data/india_housing.csv')
print(f"Loaded {len(df):,} records | {df['city'].nunique()} cities")

# ── Feature Engineering ───────────────────────────────────────
encoders = {}
cat_cols = ['city', 'locality', 'state', 'property_type', 'furnishing', 'floor']
for col in cat_cols:
    le = LabelEncoder()
    df[col + '_enc'] = le.fit_transform(df[col])
    encoders[col] = le

# Derived features
df['price_per_sqft'] = df['price'] / df['area_sqft']
df['room_ratio']     = df['bathrooms'] / df['bedrooms']
df['is_new']         = (df['age_years'] <= 3).astype(int)
df['is_luxury']      = (df['amenities_count'] >= 10).astype(int)
df['bhk_area']       = df['bedrooms'] * df['area_sqft']

FEATURES = [
    'area_sqft', 'bedrooms', 'bathrooms', 'age_years', 'garage',
    'locality_mult', 'amenities_count', 'tier',
    'city_enc', 'locality_enc', 'property_type_enc',
    'furnishing_enc', 'floor_enc',
    'room_ratio', 'is_new', 'is_luxury', 'bhk_area'
]

X = df[FEATURES]
y = df['price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Train: {len(X_train):,} | Test: {len(X_test):,}")

# ── Model Training ────────────────────────────────────────────
models = {
    'Linear Regression':  LinearRegression(),
    'Random Forest':      RandomForestRegressor(n_estimators=300, max_depth=None,
                                                min_samples_leaf=2, random_state=42, n_jobs=-1),
    'Gradient Boosting':  GradientBoostingRegressor(n_estimators=500, max_depth=5,
                                                     learning_rate=0.05, subsample=0.8,
                                                     min_samples_leaf=5, random_state=42),
}

results = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    mae   = mean_absolute_error(y_test, preds)
    rmse  = np.sqrt(mean_squared_error(y_test, preds))
    r2    = r2_score(y_test, preds)
    mape  = np.mean(np.abs((y_test - preds) / y_test)) * 100
    results[name] = {'MAE': round(mae), 'RMSE': round(rmse), 'R2': round(r2,4), 'MAPE': round(mape,2)}
    print(f"{name:22s} R²={r2:.4f}  MAE=₹{mae/1e5:.1f}L  MAPE={mape:.1f}%")

best_name = max(results, key=lambda k: results[k]['R2'])
best_model = models[best_name]
print(f"\nBest: {best_name}")

# ── EDA Plots ────────────────────────────────────────────────
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.patch.set_facecolor('#0f172a')
for ax in axes.flat:
    ax.set_facecolor('#1e293b')
    ax.tick_params(colors='#94a3b8')
    ax.xaxis.label.set_color('#94a3b8')
    ax.yaxis.label.set_color('#94a3b8')
    ax.title.set_color('#f1f5f9')
    for spine in ax.spines.values():
        spine.set_edgecolor('#334155')

colors = ['#6366f1','#06b6d4','#10b981','#f59e0b','#f43f5e','#8b5cf6']

# Price Distribution (convert rupees -> crores: 1 Cr = 1e7 INR)
axes[0,0].hist(df['price']/1e7, bins=50, color='#6366f1', alpha=0.85, edgecolor='none')
axes[0,0].set_title('Price Distribution')
axes[0,0].set_xlabel('Price (₹ Crore)')
axes[0,0].set_ylabel('Count')
axes[0,0].axvline(df['price'].median()/1e7, color='#f59e0b', linestyle='--', lw=1.5, label=f"Median")
axes[0,0].legend(labelcolor='#94a3b8', facecolor='#1e293b', edgecolor='#334155')

# Avg Price by City (top 12)
city_avg = df.groupby('city')['price'].median().sort_values(ascending=False).head(12)
bars = axes[0,1].barh(city_avg.index, city_avg.values/1e7, color='#06b6d4', alpha=0.85)
axes[0,1].set_title('Median Price by City (Top 12)')
axes[0,1].set_xlabel('Median Price (₹ Crore)')

# Price per SqFt by Tier
tier_data = [df[df['tier']==1]['price_per_sqft'], df[df['tier']==2]['price_per_sqft']]
bp = axes[0,2].boxplot( 
    tier_data,
    patch_artist=True,
    tick_labels=['Tier 1', 'Tier 2']
)
for patch, color in zip(bp['boxes'], ['#6366f1','#10b981']):
    patch.set_facecolor(color); patch.set_alpha(0.7)
for element in ['whiskers','caps','medians','fliers']:
    for item in bp[element]:
        item.set(color='#94a3b8', linewidth=1.2)
axes[0,2].set_title('Price/SqFt by Tier')
axes[0,2].set_ylabel('₹ per sq ft')

# Area vs Price scatter (price in crores)
sample = df.sample(500, random_state=42)
scatter = axes[1,0].scatter(sample['area_sqft'], sample['price']/1e7,
    c=sample['tier'], cmap='plasma', alpha=0.5, s=15)
axes[1,0].set_title('Area vs Price')
axes[1,0].set_xlabel('Area (sq ft)')
axes[1,0].set_ylabel('Price (₹ Crore)')

# Property type avg price
prop_avg = df.groupby('property_type')['price'].median().sort_values(ascending=True)
axes[1,1].barh(prop_avg.index, prop_avg.values/1e7, color='#8b5cf6', alpha=0.85)
axes[1,1].set_title('Median Price by Property Type')
axes[1,1].set_xlabel('Median Price (₹ Crore)')

# Correlation heatmap
num_cols = ['area_sqft','bedrooms','bathrooms','age_years','amenities_count',
            'locality_mult','price_per_sqft']
corr = df[num_cols].corr()
im = axes[1,2].imshow(corr, cmap='RdYlBu', vmin=-1, vmax=1, aspect='auto')
axes[1,2].set_xticks(range(len(num_cols)))
axes[1,2].set_yticks(range(len(num_cols)))
labels = ['Area','Beds','Baths','Age','Amenities','Loc Mult','Price/SqFt']
axes[1,2].set_xticklabels(labels, rotation=45, ha='right', fontsize=8, color='#94a3b8')
axes[1,2].set_yticklabels(labels, fontsize=8, color='#94a3b8')
for i in range(len(num_cols)):
    for j in range(len(num_cols)):
        axes[1,2].text(j, i, f'{corr.iloc[i,j]:.2f}', ha='center', va='center',
                       fontsize=7, color='white' if abs(corr.iloc[i,j])>0.5 else '#334155')
axes[1,2].set_title('Feature Correlation')

plt.tight_layout(pad=2)
plt.savefig('static/eda_plots.png', dpi=120, bbox_inches='tight', facecolor='#0f172a')
plt.close()

# Feature Importance
if hasattr(best_model, 'feature_importances_'):
    fi = pd.DataFrame({'feature': FEATURES, 'importance': best_model.feature_importances_})
    fi = fi.sort_values('importance', ascending=True).tail(12)
    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor('#0f172a'); ax.set_facecolor('#1e293b')
    ax.barh(fi['feature'], fi['importance'], color='#6366f1', alpha=0.85)
    ax.set_title('Feature Importance', color='#f1f5f9')
    ax.tick_params(colors='#94a3b8'); ax.xaxis.label.set_color('#94a3b8')
    for spine in ax.spines.values(): spine.set_edgecolor('#334155')
    plt.tight_layout()
    plt.savefig('static/feature_importance.png', dpi=120, bbox_inches='tight', facecolor='#0f172a')
    plt.close()

# Actual vs Predicted (values in crores)
preds_best = best_model.predict(X_test)
fig, ax = plt.subplots(figsize=(7, 5))
fig.patch.set_facecolor('#0f172a'); ax.set_facecolor('#1e293b')
ax.scatter(y_test/1e7, preds_best/1e7, alpha=0.35, c='#6366f1', s=12)
mn, mx = y_test.min()/1e7, y_test.max()/1e7
ax.plot([mn,mx],[mn,mx],'r--', lw=1.5, label='Perfect fit')
ax.set_xlabel('Actual (₹ Crore)', color='#94a3b8')
ax.set_ylabel('Predicted (₹ Crore)', color='#94a3b8')
ax.set_title('Actual vs Predicted', color='#f1f5f9')
ax.tick_params(colors='#94a3b8')
ax.legend(labelcolor='#94a3b8', facecolor='#1e293b', edgecolor='#334155')
for spine in ax.spines.values(): spine.set_edgecolor('#334155')
plt.tight_layout()
plt.savefig('static/actual_vs_predicted.png', dpi=120, bbox_inches='tight', facecolor='#0f172a')
plt.close()

# City Avg Price Chart (for dashboard)
city_stats = df.groupby('city').agg(
    avg_price=('price','median'),
    avg_psf=('price_per_sqft','median'),
    count=('price','count')
).reset_index().sort_values('avg_price', ascending=False)
city_stats.to_csv('data/city_stats.csv', index=False)

# Save everything
joblib.dump(best_model, 'model/model.pkl')
joblib.dump(encoders,   'model/encoders.pkl')

meta = {
    'best_model': best_name,
    'features': FEATURES,
    'metrics': results[best_name],
    'all_results': results,
    'n_cities': int(df['city'].nunique()),
    'n_records': int(len(df)),
    'city_list': sorted(df['city'].unique().tolist()),
}
with open('model/metadata.json','w') as f:
    json.dump(meta, f, indent=2)

print("\nAll assets saved.")
print(f"R²: {results[best_name]['R2']} | MAPE: {results[best_name]['MAPE']}%")
