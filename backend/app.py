import warnings; warnings.filterwarnings("ignore")
from flask import Flask, request, jsonify, render_template
import joblib, json, numpy as np, pandas as pd
from waitress import serve
import os, requests, socket
from datetime import datetime, timedelta
from data.market_data import (
    CITY_BASE_PRICES, PROPERTY_TYPES, FURNISHING, FLOOR_MULT,
    AMENITIES, AMENITY_PREMIUM, get_localities, get_all_cities
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'frontend'))
MODEL_DIR = os.path.join(BASE_DIR, 'model')
DATA_DIR = os.path.join(BASE_DIR, 'data')
NEWS_CACHE_PATH = os.path.join(DATA_DIR, 'news_cache.json')
os.makedirs(os.path.dirname(NEWS_CACHE_PATH), exist_ok=True)
NEWS_API_KEY = os.getenv('NEWS_API_KEY', '').strip()
NEWS_API_URL = os.getenv('NEWS_API_URL', 'https://newsapi.org/v2/everything')
NEWS_QUERY = os.getenv('NEWS_QUERY', 'India real estate OR property OR housing market India')
NEWS_PAGE_SIZE = int(os.getenv('NEWS_PAGE_SIZE', '10'))
NEWS_CACHE_TTL_HOURS = int(os.getenv('NEWS_CACHE_TTL_HOURS', '12'))

app = Flask(
    __name__,
    template_folder=os.path.join(FRONTEND_DIR, 'templates'),
    static_folder=os.path.join(FRONTEND_DIR, 'static'),
    static_url_path='/static'
)
model    = joblib.load(os.path.join(MODEL_DIR, 'model.pkl'))
encoders = joblib.load(os.path.join(MODEL_DIR, 'encoders.pkl'))
with open(os.path.join(MODEL_DIR, 'metadata.json')) as f: meta = json.load(f)
df_all   = pd.read_csv(os.path.join(DATA_DIR, 'india_housing.csv'))


def safe_encode(enc, val):
    try: return int(enc.transform([val])[0])
    except: return 0


def normalize_news_item(item):
    title = item.get('title') or 'Real estate update'
    desc = item.get('description') or item.get('content') or ''
    source = item.get('source', {}) if isinstance(item.get('source'), dict) else {}
    source_name = source.get('name') or 'Real Estate News'
    published = item.get('publishedAt') or item.get('published_at') or ''
    if published:
        try:
            published = datetime.fromisoformat(published.replace('Z', '+00:00')).strftime('%Y-%m-%d')
        except Exception:
            published = published.split('T')[0] if 'T' in published else published
    tag = 'REAL ESTATE'
    lower = title.lower()
    if 'policy' in lower or 'rbi' in lower or 'rates' in lower:
        tag = 'POLICY'
    elif 'growth' in lower or 'demand' in lower or 'market' in lower:
        tag = 'MARKET DATA'
    elif 'investment' in lower or 'roi' in lower or 'returns' in lower:
        tag = 'INVESTMENT'
    return {
        'title': title,
        'source': source_name,
        'url': item.get('url') or item.get('link') or '#',
        'published': published,
        'tag': tag,
        'desc': desc[:220] if desc else ''
    }


def load_cached_news():
    if not os.path.exists(NEWS_CACHE_PATH):
        return {'fetched_at': None, 'articles': []}
    try:
        with open(NEWS_CACHE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {'fetched_at': None, 'articles': []}


def save_cached_news(articles):
    try:
        payload = {'fetched_at': datetime.utcnow().isoformat(), 'articles': articles}
        with open(NEWS_CACHE_PATH, 'w', encoding='utf-8') as f:
            json.dump(payload, f, indent=2)
    except Exception:
        pass


def is_news_cache_stale(cache):
    if not cache or not cache.get('fetched_at'):
        return True
    try:
        fetched_at = datetime.fromisoformat(cache['fetched_at'])
        return datetime.utcnow() - fetched_at > timedelta(hours=NEWS_CACHE_TTL_HOURS)
    except Exception:
        return True


def fetch_news_from_api():
    if not NEWS_API_KEY:
        raise RuntimeError('NEWS_API_KEY is not configured')
    params = {
        'q': NEWS_QUERY,
        'apiKey': NEWS_API_KEY,
        'language': 'en',
        'pageSize': NEWS_PAGE_SIZE,
        'sortBy': 'publishedAt'
    }
    response = requests.get(NEWS_API_URL, params=params, timeout=15)
    response.raise_for_status()
    data = response.json()
    if data.get('status') != 'ok':
        raise RuntimeError(data.get('message', 'News API returned an error'))
    items = data.get('articles', [])
    return [normalize_news_item(item) for item in items]


def fallback_news():
    return [
        {"title":"India residential sales rise 8% YoY in Q1 to 70,631 units — premium segment up 30%",
         "source":"JLL India Research","url":"https://www.jll.com/en-in/insights/market-dynamics/india-residential",
         "published":"2024-06-15","tag":"MARKET DATA",
         "desc":"Bengaluru, Chennai, Delhi NCR and Kolkata led with 12%+ price growth each. Properties above ₹1 crore saw 67% YoY surge in the ₹1.5–3 Cr segment."},
        {"title":"Mumbai property prices hit all-time high recently — Worli crosses ₹1.1 lakh per sqft",
         "source":"Verified Real Estate","url":"https://community.verified.realestate",
         "published":"2024-06-28","tag":"PRICE RECORD",
         "desc":"Mumbai Coastal Road and metro expansion are driving record prices. City recorded highest property registrations in history with MMR holding 31% market share."},
        {"title":"RBI repo rate cut to 5.75% — home loan rates now approach 7%, lowest since 2022",
         "source":"Global Property Guide","url":"https://www.globalpropertyguide.com/asia/india",
         "published":"2024-06-10","tag":"POLICY",
         "desc":"Major lenders passing on cuts — SBI, HDFC rates now between 7.1–8.5%. Analysts say this will expand buyer pool by 15–20% in mid-segment housing."},
    ]

def safe_encode(enc, val):
    try: return int(enc.transform([val])[0])
    except: return 0

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/dashboard')
def dashboard():
    return render_template('index.html', meta=meta,
        cities=get_all_cities(),
        property_types=list(PROPERTY_TYPES.keys()),
        furnishing_opts=list(FURNISHING.keys()),
        floor_opts=list(FLOOR_MULT.keys()),
        amenities_list=AMENITIES)

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        d          = request.get_json()
        city       = d['city']; locality = d.get('locality','City Centre')
        prop_type  = d.get('property_type','Apartment')
        furnish    = d.get('furnishing','Semi-Furnished')
        floor      = d.get('floor','Mid (4-8)')
        area       = float(d['area_sqft']); bedrooms = int(d['bedrooms'])
        bathrooms  = int(d['bathrooms']); age = int(d['age_years'])
        garage     = int(d.get('garage',1)); amenities = int(d.get('amenities_count',5))
        city_data  = CITY_BASE_PRICES.get(city,{"tier":2})
        locs       = get_localities(city)
        loc_mult   = locs.get(locality,1.0); tier = city_data.get('tier',2)
        FEATS      = ['area_sqft','bedrooms','bathrooms','age_years','garage','locality_mult',
                      'amenities_count','tier','city_enc','locality_enc','property_type_enc',
                      'furnishing_enc','floor_enc','room_ratio','is_new','is_luxury','bhk_area']
        features   = pd.DataFrame([[area,bedrooms,bathrooms,age,garage,loc_mult,amenities,tier,
            safe_encode(encoders['city'],city), safe_encode(encoders['locality'],locality),
            safe_encode(encoders['property_type'],prop_type), safe_encode(encoders['furnishing'],furnish),
            safe_encode(encoders['floor'],floor),
            bathrooms/max(bedrooms,1), 1 if age<=3 else 0, 1 if amenities>=10 else 0, bedrooms*area
        ]], columns=FEATS)
        price = max(float(model.predict(features)[0]),200000)
        mape  = meta['metrics']['MAPE']/100
        growth= CITY_BASE_PRICES.get(city,{}).get('growth_yoy',8)
        score = min(100,int(growth*4+(1 if age<=3 else 0)*10+min(amenities*1.5,20)+(10 if tier==1 else 5)))
        return jsonify({'predicted_price':round(price),'low_estimate':round(price*(1-mape*.8)),
            'high_estimate':round(price*(1+mape*.8)),'price_per_sqft':round(price/area),
            'investment_score':score,'growth_yoy':growth,
            'city_avg_psf':CITY_BASE_PRICES.get(city,{}).get('avg',5000),'model_used':meta['best_model']})
    except Exception as e: return jsonify({'error':str(e)}),400

@app.route('/api/localities/<city>')
def localities(city):
    return jsonify({'localities':list(get_localities(city).keys())})

@app.route('/api/city-stats')
def city_stats():
    return jsonify(sorted([{'city':c,'state':d['state'],'tier':d['tier'],'avg_psf':d['avg'],
        'min_psf':d['min'],'max_psf':d['max'],'growth_yoy':d['growth_yoy']}
        for c,d in CITY_BASE_PRICES.items()],key=lambda x:-x['avg_psf']))

@app.route('/api/compare', methods=['POST'])
def compare():
    cities = request.get_json().get('cities',[])
    return jsonify([{'city':c,'state':CITY_BASE_PRICES[c]['state'],'tier':CITY_BASE_PRICES[c]['tier'],
        'avg_psf':CITY_BASE_PRICES[c]['avg'],'min_psf':CITY_BASE_PRICES[c]['min'],
        'max_psf':CITY_BASE_PRICES[c]['max'],'growth_yoy':CITY_BASE_PRICES[c]['growth_yoy']}
        for c in cities if c in CITY_BASE_PRICES])

@app.route('/api/roi', methods=['POST'])
def roi():
    d=request.get_json(); city=d.get('city','Bengaluru')
    purchase=float(d.get('purchase_price',5000000)); hold=int(d.get('hold_years',5))
    rent=float(d.get('monthly_rent',25000)); loan_p=float(d.get('loan_percent',80))/100
    rate=float(d.get('interest_rate',8.5))/100
    growth=CITY_BASE_PRICES.get(city,{}).get('growth_yoy',8)/100
    fv=purchase*((1+growth)**hold); cg=fv-purchase; ri=rent*12*hold
    loan=purchase*loan_p; mr=rate/12; n=hold*12
    emi=(loan*mr*(1+mr)**n)/((1+mr)**n-1) if mr>0 else loan/n
    ti=emi*n-loan; nr=cg+ri-ti
    return jsonify({'future_value':round(fv),'capital_gain':round(cg),'rental_income':round(ri),
        'total_interest':round(ti),'net_return':round(nr),'roi_percent':round((nr/purchase)*100,2),
        'annual_roi':round((nr/purchase)*100/hold,2),'monthly_emi':round(emi),
        'growth_rate':growth*100,
        'yearly':[{'year':y,'property_value':round(purchase*((1+growth)**y)),'cumulative_rent':round(rent*12*y)} for y in range(1,hold+1)]})

@app.route('/api/trends')
def trends():
    import random; random.seed(42)
    quarters=['Q1 20','Q2 20','Q3 20','Q4 20','Q1 21','Q2 21','Q3 21','Q4 21',
               'Q1 22','Q2 22','Q3 22','Q4 22','Q1 23','Q2 23','Q3 23','Q4 23',
               'Q1 24','Q2 24','Q3 24','Q4 24','Q1 25','Q2 25','Q3 25','Q4 25','Q1 26']
    mults=[1.00,0.96,0.93,0.95,0.98,1.01,1.05,1.09,1.14,1.19,1.24,1.30,
           1.36,1.41,1.47,1.54,1.61,1.67,1.74,1.82,1.89,1.96,2.03,2.11,2.20]
    cities=['Mumbai','Bengaluru','Hyderabad','Delhi','Pune','Chennai']
    return jsonify({'quarters':quarters,'cities':{
        c:[round(CITY_BASE_PRICES[c]['avg']*mults[i]*random.uniform(.97,1.03)) for i in range(len(quarters))]
        for c in cities}})

@app.route('/api/news')
def news():
    cache = load_cached_news()
    if is_news_cache_stale(cache):
        try:
            articles = fetch_news_from_api()
            if articles:
                save_cached_news(articles)
                return jsonify(articles)
        except Exception:
            pass
    if cache and cache.get('articles'):
        return jsonify(cache['articles'])
    return jsonify(fallback_news())

@app.route('/api/model-info')
def model_info(): return jsonify(meta)


def find_free_port(start_port=5001, max_port=5010):
    for port in range(start_port, max_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                s.bind(('0.0.0.0', port))
                return port
            except OSError:
                continue
    raise RuntimeError(f'No free ports available between {start_port} and {max_port}')


if __name__=='__main__':
    print(f"PropWise India | {meta['best_model']} R²={meta['metrics']['R2']} | {meta['n_cities']} cities")
    
    port_env = os.getenv('PORT')
    port = int(port_env) if port_env else 5001
    
    if not port_env:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(('0.0.0.0', port))
        except OSError:
            port = find_free_port(port + 1, port + 10)
            print(f'Port 5001 in use, starting on port {port} instead.')
            
    print(f"Starting production server on http://localhost:{port}")
    serve(app, host='0.0.0.0', port=port)
