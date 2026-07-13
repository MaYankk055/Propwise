"""
India Real Estate Market Data —
Sources: JLL Q1, Anarock, Colliers India, PropTiger, NHB Residex
60+ cities across all tiers
"""

CITY_BASE_PRICES = {
    # ── Tier 1 Metros ──────────────────────────────────────────
    "Mumbai":            {"min":18000,"max":110000,"avg":32000,"tier":1,"state":"Maharashtra","growth_yoy":14.2,"lat":19.076,"lng":72.877},
    "Delhi":             {"min":9000, "max":42000, "avg":16000,"tier":1,"state":"Delhi",      "growth_yoy":13.5,"lat":28.613,"lng":77.209},
    "Bengaluru":         {"min":6000, "max":26000, "avg":10500,"tier":1,"state":"Karnataka",  "growth_yoy":15.8,"lat":12.972,"lng":77.594},
    "Hyderabad":         {"min":5000, "max":20000, "avg":8800, "tier":1,"state":"Telangana",  "growth_yoy":8.0, "lat":17.385,"lng":78.486},
    "Chennai":           {"min":5500, "max":20000, "avg":9000, "tier":1,"state":"Tamil Nadu", "growth_yoy":13.2,"lat":13.083,"lng":80.270},
    "Kolkata":           {"min":4000, "max":16000, "avg":7000, "tier":1,"state":"West Bengal","growth_yoy":12.4,"lat":22.572,"lng":88.363},
    "Pune":              {"min":6000, "max":22000, "avg":9500, "tier":1,"state":"Maharashtra","growth_yoy":11.2,"lat":18.520,"lng":73.856},
    "Ahmedabad":         {"min":4000, "max":14000, "avg":6500, "tier":1,"state":"Gujarat",    "growth_yoy":10.5,"lat":23.022,"lng":72.571},
    "Navi Mumbai":       {"min":9000, "max":28000, "avg":15500,"tier":1,"state":"Maharashtra","growth_yoy":9.8, "lat":19.033,"lng":73.029},
    "Gurgaon":           {"min":8000, "max":32000, "avg":15000,"tier":1,"state":"Haryana",    "growth_yoy":13.8,"lat":28.459,"lng":77.026},
    "Noida":             {"min":6000, "max":20000, "avg":10000,"tier":1,"state":"UP",         "growth_yoy":11.5,"lat":28.535,"lng":77.391},
    # ── Tier 2 ────────────────────────────────────────────────
    "Jaipur":            {"min":3500, "max":11000, "avg":5500, "tier":2,"state":"Rajasthan",  "growth_yoy":10.2,"lat":26.912,"lng":75.787},
    "Lucknow":           {"min":3000, "max":9500,  "avg":4800, "tier":2,"state":"UP",         "growth_yoy":9.1, "lat":26.846,"lng":80.946},
    "Kochi":             {"min":5000, "max":16000, "avg":7500, "tier":2,"state":"Kerala",     "growth_yoy":10.8,"lat":9.931, "lng":76.267},
    "Chandigarh":        {"min":4500, "max":15000, "avg":7200, "tier":2,"state":"Chandigarh", "growth_yoy":8.7, "lat":30.733,"lng":76.779},
    "Coimbatore":        {"min":3500, "max":11000, "avg":5800, "tier":2,"state":"Tamil Nadu", "growth_yoy":12.1,"lat":11.016,"lng":76.955},
    "Nagpur":            {"min":3000, "max":9000,  "avg":4600, "tier":2,"state":"Maharashtra","growth_yoy":7.9, "lat":21.145,"lng":79.088},
    "Indore":            {"min":2800, "max":9000,  "avg":4500, "tier":2,"state":"MP",         "growth_yoy":13.0,"lat":22.719,"lng":75.857},
    "Bhopal":            {"min":2500, "max":8000,  "avg":4000, "tier":2,"state":"MP",         "growth_yoy":9.3, "lat":23.259,"lng":77.413},
    "Visakhapatnam":     {"min":3200, "max":10000, "avg":5200, "tier":2,"state":"Andhra",     "growth_yoy":11.0,"lat":17.686,"lng":83.218},
    "Surat":             {"min":3200, "max":11000, "avg":5500, "tier":2,"state":"Gujarat",    "growth_yoy":11.8,"lat":21.170,"lng":72.831},
    "Vadodara":          {"min":3000, "max":9000,  "avg":4800, "tier":2,"state":"Gujarat",    "growth_yoy":9.6, "lat":22.307,"lng":73.181},
    "Nashik":            {"min":3200, "max":9500,  "avg":5000, "tier":2,"state":"Maharashtra","growth_yoy":10.5,"lat":19.997,"lng":73.790},
    "Mysuru":            {"min":3800, "max":12000, "avg":6200, "tier":2,"state":"Karnataka",  "growth_yoy":12.8,"lat":12.295,"lng":76.639},
    "Thiruvananthapuram":{"min":4000, "max":12000, "avg":6400, "tier":2,"state":"Kerala",     "growth_yoy":9.5, "lat":8.524, "lng":76.936},
    "Patna":             {"min":2800, "max":8000,  "avg":4200, "tier":2,"state":"Bihar",      "growth_yoy":8.2, "lat":25.594,"lng":85.137},
    "Dehradun":          {"min":3200, "max":10000, "avg":5500, "tier":2,"state":"Uttarakhand","growth_yoy":14.0,"lat":30.316,"lng":78.032},
    "Raipur":            {"min":2400, "max":7500,  "avg":3900, "tier":2,"state":"Chhattisgarh","growth_yoy":8.8,"lat":21.251,"lng":81.629},
    "Bhubaneswar":       {"min":3200, "max":9500,  "avg":5200, "tier":2,"state":"Odisha",     "growth_yoy":11.2,"lat":20.296,"lng":85.824},
    "Guwahati":          {"min":3000, "max":9000,  "avg":4700, "tier":2,"state":"Assam",      "growth_yoy":10.1,"lat":26.144,"lng":91.736},
    "Amritsar":          {"min":2700, "max":8000,  "avg":4300, "tier":2,"state":"Punjab",     "growth_yoy":7.5, "lat":31.634,"lng":74.872},
    "Rajkot":            {"min":2700, "max":8500,  "avg":4400, "tier":2,"state":"Gujarat",    "growth_yoy":9.4, "lat":22.303,"lng":70.802},
    "Faridabad":         {"min":5000, "max":15000, "avg":8000, "tier":2,"state":"Haryana",    "growth_yoy":10.6,"lat":28.408,"lng":77.317},
    "Meerut":            {"min":3000, "max":8500,  "avg":4600, "tier":2,"state":"UP",         "growth_yoy":8.1, "lat":28.984,"lng":77.706},
    "Agra":              {"min":2500, "max":7500,  "avg":4000, "tier":2,"state":"UP",         "growth_yoy":7.8, "lat":27.176,"lng":78.008},
    "Varanasi":          {"min":2800, "max":8500,  "avg":4500, "tier":2,"state":"UP",         "growth_yoy":9.0, "lat":25.317,"lng":82.973},
    "Kanpur":            {"min":2500, "max":7000,  "avg":3800, "tier":2,"state":"UP",         "growth_yoy":7.2, "lat":26.449,"lng":80.331},
    "Aurangabad":        {"min":2800, "max":8000,  "avg":4200, "tier":2,"state":"Maharashtra","growth_yoy":8.5, "lat":19.876,"lng":75.343},
    "Madurai":           {"min":3000, "max":9000,  "avg":4800, "tier":2,"state":"Tamil Nadu", "growth_yoy":9.2, "lat":9.925, "lng":78.119},
    "Tiruchirappalli":   {"min":2800, "max":8000,  "avg":4400, "tier":2,"state":"Tamil Nadu", "growth_yoy":8.8, "lat":10.790,"lng":78.704},
    "Hubli-Dharwad":     {"min":2500, "max":7500,  "avg":3900, "tier":2,"state":"Karnataka",  "growth_yoy":8.3, "lat":15.360,"lng":75.124},
    "Mangaluru":         {"min":3500, "max":10500, "avg":5800, "tier":2,"state":"Karnataka",  "growth_yoy":10.3,"lat":12.914,"lng":74.856},
    "Warangal":          {"min":2500, "max":7000,  "avg":3800, "tier":2,"state":"Telangana",  "growth_yoy":8.0, "lat":17.977,"lng":79.598},
    "Vijayawada":        {"min":3200, "max":9500,  "avg":5200, "tier":2,"state":"Andhra",     "growth_yoy":10.5,"lat":16.506,"lng":80.648},
    "Guntur":            {"min":2800, "max":8000,  "avg":4300, "tier":2,"state":"Andhra",     "growth_yoy":9.1, "lat":16.306,"lng":80.436},
    "Jodhpur":           {"min":2500, "max":8000,  "avg":4200, "tier":2,"state":"Rajasthan",  "growth_yoy":8.9, "lat":26.294,"lng":73.044},
    "Udaipur":           {"min":3000, "max":9500,  "avg":5000, "tier":2,"state":"Rajasthan",  "growth_yoy":10.7,"lat":24.585,"lng":73.712},
    "Kota":              {"min":2500, "max":7000,  "avg":3700, "tier":2,"state":"Rajasthan",  "growth_yoy":7.5, "lat":25.215,"lng":75.865},
    "Jabalpur":          {"min":2200, "max":7000,  "avg":3600, "tier":2,"state":"MP",         "growth_yoy":7.8, "lat":23.181,"lng":79.987},
    "Gwalior":           {"min":2200, "max":6500,  "avg":3400, "tier":2,"state":"MP",         "growth_yoy":7.0, "lat":26.218,"lng":78.182},
    "Ludhiana":          {"min":3000, "max":9000,  "avg":5000, "tier":2,"state":"Punjab",     "growth_yoy":8.2, "lat":30.901,"lng":75.857},
    "Jalandhar":         {"min":2700, "max":8000,  "avg":4300, "tier":2,"state":"Punjab",     "growth_yoy":7.8, "lat":31.326,"lng":75.576},
    "Shimla":            {"min":4000, "max":12000, "avg":6500, "tier":2,"state":"Himachal",   "growth_yoy":11.5,"lat":31.104,"lng":77.173},
    "Jammu":             {"min":3000, "max":9000,  "avg":4800, "tier":2,"state":"J&K",        "growth_yoy":9.2, "lat":32.726,"lng":74.857},
    "Ranchi":            {"min":2500, "max":7500,  "avg":4000, "tier":2,"state":"Jharkhand",  "growth_yoy":8.5, "lat":23.344,"lng":85.309},
    "Jamshedpur":        {"min":2800, "max":8000,  "avg":4400, "tier":2,"state":"Jharkhand",  "growth_yoy":8.0, "lat":22.804,"lng":86.203},
    "Cuttack":           {"min":2700, "max":7500,  "avg":4000, "tier":2,"state":"Odisha",     "growth_yoy":8.3, "lat":20.462,"lng":85.883},
    "Kozhikode":         {"min":3800, "max":11000, "avg":6000, "tier":2,"state":"Kerala",     "growth_yoy":9.8, "lat":11.258,"lng":75.780},
    "Thrissur":          {"min":4000, "max":12000, "avg":6500, "tier":2,"state":"Kerala",     "growth_yoy":10.2,"lat":10.527,"lng":76.214},
    "Salem":             {"min":2800, "max":8000,  "avg":4500, "tier":2,"state":"Tamil Nadu", "growth_yoy":9.0, "lat":11.664,"lng":78.146},
    "Tirunelveli":       {"min":2500, "max":7500,  "avg":4000, "tier":2,"state":"Tamil Nadu", "growth_yoy":8.5, "lat":8.727, "lng":77.696},
    "Pondicherry":       {"min":3500, "max":11000, "avg":6000, "tier":2,"state":"Puducherry", "growth_yoy":11.0,"lat":11.934,"lng":79.830},
    "Nanded":            {"min":2200, "max":6500,  "avg":3500, "tier":2,"state":"Maharashtra","growth_yoy":7.2, "lat":19.147,"lng":77.321},
    "Kolhapur":          {"min":2800, "max":8500,  "avg":4600, "tier":2,"state":"Maharashtra","growth_yoy":9.1, "lat":16.705,"lng":74.243},
    "Solapur":           {"min":2500, "max":7000,  "avg":3800, "tier":2,"state":"Maharashtra","growth_yoy":7.8, "lat":17.686,"lng":75.906},
    "Prayagraj":         {"min":2500, "max":7500,  "avg":4000, "tier":2,"state":"UP",         "growth_yoy":8.0, "lat":25.4358,"lng":81.8463},
    "Bareilly":          {"min":2200, "max":6000,  "avg":3500, "tier":2,"state":"UP",         "growth_yoy":7.0, "lat":28.3670,"lng":79.4304},
    "Aligarh":           {"min":2000, "max":5500,  "avg":3300, "tier":2,"state":"UP",         "growth_yoy":6.5, "lat":27.8974,"lng":78.0880},
    "Moradabad":         {"min":2100, "max":5800,  "avg":3400, "tier":2,"state":"UP",         "growth_yoy":6.8, "lat":28.8386,"lng":78.7733},
    "Gorakhpur":         {"min":2400, "max":6500,  "avg":3600, "tier":2,"state":"UP",         "growth_yoy":7.5, "lat":26.7606,"lng":83.3732},
    "Bikaner":           {"min":2200, "max":6000,  "avg":3500, "tier":2,"state":"Rajasthan",  "growth_yoy":7.1, "lat":28.0229,"lng":73.3119},
    "Ajmer":             {"min":2300, "max":6200,  "avg":3600, "tier":2,"state":"Rajasthan",  "growth_yoy":7.4, "lat":26.4499,"lng":74.6399},
    "Belagavi":          {"min":2400, "max":6800,  "avg":3800, "tier":2,"state":"Karnataka",  "growth_yoy":8.2, "lat":15.8497,"lng":74.4977},
    "Gandhinagar":       {"min":3000, "max":10000, "avg":5500, "tier":2,"state":"Gujarat",    "growth_yoy":12.5,"lat":23.2156,"lng":72.6369},
    "Bhavnagar":         {"min":2200, "max":6000,  "avg":3400, "tier":2,"state":"Gujarat",    "growth_yoy":8.0, "lat":21.7645,"lng":72.1519},
    "Jamnagar":          {"min":2100, "max":5800,  "avg":3200, "tier":2,"state":"Gujarat",    "growth_yoy":7.5, "lat":22.4707,"lng":70.0577},
    "Junagadh":          {"min":1800, "max":5000,  "avg":2800, "tier":2,"state":"Gujarat",    "growth_yoy":6.5, "lat":21.5222,"lng":70.4579},
    "Anand":             {"min":2000, "max":5500,  "avg":3000, "tier":2,"state":"Gujarat",    "growth_yoy":7.0, "lat":22.5645,"lng":72.9289},
    "Navsari":           {"min":1900, "max":5200,  "avg":2900, "tier":2,"state":"Gujarat",    "growth_yoy":6.8, "lat":20.9467,"lng":72.9520},
    "Bharuch":           {"min":2000, "max":5300,  "avg":3100, "tier":2,"state":"Gujarat",    "growth_yoy":7.2, "lat":21.7051,"lng":72.9959},
    "Vapi":              {"min":2200, "max":5800,  "avg":3300, "tier":2,"state":"Gujarat",    "growth_yoy":7.8, "lat":20.3893,"lng":72.9106},
    "Bhuj":              {"min":1800, "max":4800,  "avg":2700, "tier":2,"state":"Gujarat",    "growth_yoy":6.0, "lat":23.2420,"lng":69.6669},
    "Porbandar":         {"min":1700, "max":4500,  "avg":2600, "tier":2,"state":"Gujarat",    "growth_yoy":5.5, "lat":21.6417,"lng":69.6293},
    "Morbi":             {"min":1900, "max":5000,  "avg":2800, "tier":2,"state":"Gujarat",    "growth_yoy":6.2, "lat":22.8120,"lng":70.8320},
}

CITY_LOCALITIES = {
    "Mumbai":        {"Worli":3.4,"Bandra":2.8,"Juhu":2.5,"Lower Parel":2.2,"Kohinoor Square":2.0,"Powai":1.4,"Andheri":1.2,"Mulund":0.85,"Borivali":0.8,"Thane":0.75,"Mira Road":0.6,"Virar":0.5},
    "Delhi":         {"Lutyens Delhi":3.2,"South Delhi":2.3,"Vasant Kunj":2.0,"Saket":1.9,"Lajpat Nagar":1.7,"Dwarka":1.0,"Rohini":0.9,"Janakpuri":1.1,"Pitampura":0.9,"Shahdara":0.75},
    "Bengaluru":     {"Indiranagar":2.0,"Koramangala":1.9,"Whitefield":1.5,"HSR Layout":1.7,"Electronic City":0.9,"Hebbal":1.2,"Sarjapur":1.1,"JP Nagar":1.3,"Marathahalli":1.2,"Yelahanka":0.85,"Kengeri":0.7},
    "Hyderabad":     {"Jubilee Hills":2.2,"Banjara Hills":2.0,"HITEC City":1.6,"Gachibowli":1.5,"Kondapur":1.3,"Madhapur":1.4,"Miyapur":0.95,"Kukatpally":1.1,"LB Nagar":0.8,"Kompally":0.9},
    "Chennai":       {"Nungambakkam":2.1,"Adyar":2.0,"Anna Nagar":1.7,"Velachery":1.2,"OMR":1.1,"Sholinganallur":1.1,"Porur":0.95,"Tambaram":0.8,"Perambur":0.85,"Guindy":1.3},
    "Pune":          {"Koregaon Park":2.0,"Kalyani Nagar":1.8,"Viman Nagar":1.5,"Baner":1.4,"Hinjewadi":1.2,"Kharadi":1.3,"Wakad":1.1,"Hadapsar":0.95,"Pimple Saudagar":1.0,"Kondhwa":0.9},
    "Kolkata":       {"Park Street":2.2,"Alipore":2.3,"Ballygunge":1.9,"Salt Lake":1.4,"New Town":1.3,"Rajarhat":1.0,"Tollygunge":1.1,"Behala":0.8,"Howrah":0.7},
    "Ahmedabad":     {"SG Highway":1.6,"Prahlad Nagar":1.7,"Satellite":1.5,"Bopal":1.2,"Thaltej":1.3,"Vastrapur":1.4,"Gota":0.95,"Chandkheda":0.9,"Maninagar":0.85},
    "Gurgaon":       {"Golf Course Road":2.2,"DLF Cyber City":2.0,"MG Road":1.7,"Sohna Road":1.2,"Palam Vihar":1.0,"Sector 57":1.2,"Sector 49":1.1,"Sector 82":0.9,"Manesar":0.75},
    "Noida":         {"Sector 44":1.5,"Sector 50":1.4,"Sector 150":1.2,"Sector 62":1.2,"Sector 18":1.3,"Greater Noida West":0.8,"Sector 76":0.95,"Yamuna Expressway":0.7},
    "Jaipur":        {"C Scheme":2.0,"Vaishali Nagar":1.5,"Mansarovar":1.2,"Malviya Nagar":1.3,"Jagatpura":1.0,"Pratap Nagar":0.9,"Ajmer Road":0.85,"Tonk Road":1.1},
    "Kochi":         {"Marine Drive":2.1,"Kakkanad":1.3,"Edapally":1.2,"Vyttila":1.4,"Thrippunithura":1.0,"Maradu":1.1,"Aluva":0.9,"Cheranalloor":0.85},
    "Dehradun":      {"Rajpur Road":1.8,"Sahastradhara":1.4,"Vasant Vihar":1.6,"ISBT":1.1,"Prem Nagar":0.9,"Raipur":1.0},
    "Gandhinagar":   {"GIFT City":2.2, "Kudasan":1.5, "Sargasan":1.4, "Randesan":1.2, "Infocity":1.3, "Sector 11":1.1},
}

DEFAULT_LOCALITIES = {"City Centre":1.7,"Prime Location":2.0,"Main Road":1.4,"Residential Area":1.0,"Suburban":0.85,"Outskirts":0.7,"New Township":1.1,"Tech Park Area":1.3}

PROPERTY_TYPES   = {"Apartment":1.0,"Villa":1.5,"Independent House":1.2,"Builder Floor":0.9,"Studio":0.85,"Penthouse":2.2,"Row House":1.15,"Duplex":1.3}
FURNISHING       = {"Unfurnished":1.0,"Semi-Furnished":1.12,"Fully Furnished":1.28}
FLOOR_MULT       = {"Ground":0.92,"Low (1-3)":0.97,"Mid (4-8)":1.0,"High (9-15)":1.06,"Top Floor":1.10,"Penthouse":1.22}
AMENITIES        = ["Swimming Pool","Gym","Club House","24hr Security","Power Backup","Car Parking","Children Play Area","Garden/Park","Lift","CCTV","Intercom","Visitor Parking","Jogging Track","Tennis Court","Indoor Games"]
AMENITY_PREMIUM  = 0.018

def get_localities(city):  return CITY_LOCALITIES.get(city, DEFAULT_LOCALITIES)
def get_price_range(city):
    d = CITY_BASE_PRICES.get(city, {"min":2000,"max":8000,"avg":4000})
    return d["min"], d["max"], d["avg"]
def get_all_cities(): return sorted(CITY_BASE_PRICES.keys())
