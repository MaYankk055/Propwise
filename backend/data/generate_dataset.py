"""
Generate realistic India housing dataset based on actual 2024 market rates.
Uses city-specific base prices, locality multipliers, and property features.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
import numpy as np
import os
from data.market_data import (
    CITY_BASE_PRICES, CITY_LOCALITIES, DEFAULT_LOCALITIES,
    PROPERTY_TYPES, FURNISHING, FLOOR_MULT, AMENITIES, AMENITY_PREMIUM
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = BASE_DIR

np.random.seed(42)
records = []

for city, city_data in CITY_BASE_PRICES.items():
    n_samples = 120 if city_data["tier"] == 1 else 70
    localities = CITY_LOCALITIES.get(city, DEFAULT_LOCALITIES)
    loc_names = list(localities.keys())
    loc_mults = list(localities.values())

    for _ in range(n_samples):
        # Features
        area = int(np.random.choice([
            np.random.randint(400, 800),
            np.random.randint(800, 1500),
            np.random.randint(1500, 3000),
            np.random.randint(3000, 6000)
        ], p=[0.25, 0.40, 0.25, 0.10]))

        bedrooms  = np.random.choice([1,2,3,4,5], p=[0.12, 0.35, 0.35, 0.13, 0.05])
        bathrooms = min(bedrooms + np.random.choice([0,1], p=[0.6,0.4]), 5)
        age       = int(np.random.choice(
            [np.random.randint(0,2), np.random.randint(2,8),
             np.random.randint(8,20), np.random.randint(20,45)],
            p=[0.2, 0.35, 0.3, 0.15]
        ))
        garage    = np.random.choice([0,1,2], p=[0.25, 0.55, 0.20])
        prop_type = np.random.choice(list(PROPERTY_TYPES.keys()),
                                     p=[0.55,0.10,0.12,0.10,0.05,0.02,0.04,0.02])
        furnish   = np.random.choice(list(FURNISHING.keys()), p=[0.4, 0.35, 0.25])
        floor     = np.random.choice(list(FLOOR_MULT.keys()),
                                     p=[0.12,0.20,0.30,0.22,0.10,0.06])
        loc_idx   = np.random.choice(len(loc_names))
        locality  = loc_names[loc_idx]
        loc_mult  = loc_mults[loc_idx]
        n_amenities = int(np.random.choice(range(16),
                          p=[0.05,0.05,0.07,0.10,0.12,0.12,0.10,0.09,0.08,0.07,0.05,0.04,0.03,0.02,0.01,0.00]))

        # Price calculation
        base_psf  = city_data["avg"]
        price = (base_psf
                 * loc_mult
                 * PROPERTY_TYPES[prop_type]
                 * FURNISHING[furnish]
                 * FLOOR_MULT[floor]
                 * (1 + n_amenities * AMENITY_PREMIUM)
                 * (0.97 ** max(age - 3, 0))
                 * area)

        # BHK bedroom correction
        price *= (1 + (bedrooms - 2) * 0.04)

        # Noise ±8%
        price *= np.random.uniform(0.92, 1.08)
        price = max(int(price), 500000)

        records.append({
            "city": city,
            "locality": locality,
            "state": city_data["state"],
            "tier": city_data["tier"],
            "area_sqft": area,
            "bedrooms": int(bedrooms),
            "bathrooms": int(bathrooms),
            "age_years": age,
            "garage": int(garage),
            "property_type": prop_type,
            "furnishing": furnish,
            "floor": floor,
            "locality_mult": round(loc_mult, 2),
            "amenities_count": n_amenities,
            "price": price,
            "price_psf": round(price / area),
        })

df = pd.DataFrame(records)
os.makedirs(DATA_DIR, exist_ok=True)
df.to_csv(os.path.join(DATA_DIR, "india_housing.csv"), index=False)
print(f"Dataset: {len(df):,} records across {df['city'].nunique()} cities")
print(f"Price range: ₹{df['price'].min():,.0f} – ₹{df['price'].max():,.0f}")
print(f"Avg price/sqft by tier:")
print(df.groupby('tier')['price_psf'].mean().apply(lambda x: f"₹{x:,.0f}"))
