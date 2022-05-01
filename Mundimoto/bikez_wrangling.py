import pandas as pd
import numpy as np

bikez_df = pd.read_csv('landing/persistent/all_bikez_data.csv')
brands_df = pd.read_csv('landing/persistent/bikez_brands_data.csv')
mundimoto_df = pd.read_csv('landing/persistent/mundimoto2.csv')

# ---
# *** Preprocessing mundimoto_df ***
# ---

# concat model and version to form model
mundimoto_df["Model"] = mundimoto_df['model'].astype(str) +" "+ mundimoto_df["version"]
mundimoto_df.drop(['model', 'version'], axis=1, inplace=True)

# renaming columns
mundimoto_df.rename(columns = {'brand':'Brand', 
                               'year':'Year', 
                               'km':'Odometer', 
                               'sell_price':'Sell_Price', 
                               'purchase_price':'Purchase_Price'}, 
                    inplace = True)

# reordering columns
mundimoto_df = mundimoto_df[['id', 'Brand', 'Model', 'Year', 'Odometer', 'Sell_Price', 'Purchase_Price']]

# mundimoto_df prep for merge
mundimoto_df.Model = mundimoto_df.Model.apply(lambda x: str(x).lower().strip())
mundimoto_df.Brand = mundimoto_df.Brand.apply(lambda x: str(x).lower().strip())
mundimoto_df.Year = mundimoto_df.Year.apply(lambda x: str(x).lower().strip())

# removing [*AJ] from model
mundimoto_df['Model'].replace('\[.*\]', '', regex=True, inplace=True)

# ---
# *** Preprocessing bikez_df ***
# ---

# Matching brand to model 
brands_df.Brand = brands_df.Brand.apply(lambda x: str(x).strip())
bikez_df.Model = bikez_df.Model.apply(lambda x: str(x).strip())

Brands = brands_df.Brand.unique()
Models = bikez_df.Model.unique()

data = {}
for model in Models:
    for brand in Brands:
        brand_peaces = brand.split(' ')
        model_peaces = model.split(' ')
        i = 0
        all = True
        for i in range(len(brand_peaces)):
            if brand_peaces[i].lower() != model_peaces[i].lower():
                # print(brand, model)
                all = False
                break
        if all:
            data[model.lower()] = brand.lower()
            break
            
df_match = pd.DataFrame(list(data.items()),columns = ['Model','Brand'])
bikez_df.Model = bikez_df.Model.apply(lambda x: str(x).lower())
bikez_df = pd.merge(bikez_df, df_match, on="Model")

# remove brand from model
bikez_df.Model = bikez_df.Model.apply(lambda x: str(x).replace(data[x], '').strip().lower())

# extract rating float
def extract_rating(x):
    if x[1].isdigit():
        return float(x[:4])
    else:
        return np.nan

bikez_df['Rating'] = bikez_df['Rating'].apply(lambda x: extract_rating(x))

# resolve displacement
bikez_df.loc[:, 'Displacement (ccm)'] = bikez_df['Displacement'].str[0:6]
bikez_df['Displacement (ccm)'].replace('c', '', regex=True, inplace=True)
bikez_df['Displacement (ccm)'] = bikez_df['Displacement (ccm)'].astype(float)
bikez_df.drop(['Displacement'], axis=1, inplace=True)

# resolve power
bikez_df.loc[:, 'Power (hp)'] = bikez_df['Power'].str[0:4]
bikez_df['Power (hp)'].replace('H', '', regex=True, inplace=True)
bikez_df['Power (hp)'] = bikez_df['Power (hp)'].astype(float)
bikez_df.drop(['Power'], axis=1, inplace=True)

# resolve torque
bikez_df.loc[:, 'Torque (Nm)'] = bikez_df['Torque'].str[0:4]
bikez_df['Torque (Nm)'].replace('N', '', regex=True, inplace=True)
bikez_df['Torque (Nm)'] = bikez_df['Torque (Nm)'].astype(float)
bikez_df.drop(['Torque'], axis=1, inplace=True)

# resolve transmission type
bikez_df['Transmission type'] = bikez_df['Transmission type'].str.split().str.join(' ')
bikez_df['Transmission type'].replace('\s*\(final drive\)', '', regex=True, inplace=True)
bikez_df['Transmission type'].replace('\s*\(cardan\)', '', regex=True, inplace=True)
bikez_df['Transmission type'].unique()

# resolve wheelbase
bikez_df.loc[:, 'Wheelbase (mm)'] = bikez_df['Wheelbase'].str[0:5]
bikez_df['Wheelbase (mm)'].replace('m', '', regex=True, inplace=True)
bikez_df['Wheelbase (mm)'] = bikez_df['Wheelbase (mm)'].astype(float)
bikez_df.drop(['Wheelbase'], axis=1, inplace=True)

# resolve fuel capacity
bikez_df.loc[:, 'Fuel capacity (lts)'] = bikez_df['Fuel capacity'].str[0:6]
bikez_df['Fuel capacity (lts)'].replace('l', '', regex=True, inplace=True)
bikez_df['Fuel capacity (lts)'] = bikez_df['Fuel capacity (lts)'].astype(float)
bikez_df.drop(['Fuel capacity'], axis=1, inplace=True)

# resolve bore x stroke
def return_stroke(x):
    values = str(x).split('x')
    if len(values) > 1:
        return values[1].strip()
    else:
        str(x).strip()

def return_bore(x):
    values = str(x).split('x')
    if len(values) > 1:
        return values[0].strip()
    else:
        str(x).strip()
        
bikez_df['Bore x stroke'].replace('\(.*\)', '', regex=True, inplace=True)
bikez_df['Bore x stroke'].replace('\s*mm\s*', '', regex=True, inplace=True)
bikez_df['Bore (mm)'] = bikez_df['Bore x stroke'].apply(lambda x: return_bore(x))
bikez_df['Stroke (mm)'] = bikez_df['Bore x stroke'].apply(lambda x: return_stroke(x))
bikez_df.drop(['Bore x stroke'], axis=1, inplace=True)

# resolve seat height
bikez_df.loc[:, 'Seat height (mm)'] = bikez_df['Seat height'].str[0:5]
bikez_df['Seat height (mm)'].replace('m', '', regex=True, inplace=True)
bikez_df['Seat height (mm)'].replace(',', '', regex=True, inplace=True)
bikez_df['Seat height (mm)'] = bikez_df['Seat height (mm)'].astype(float)
bikez_df.drop(['Seat height'], axis=1, inplace=True)

# split engine_type
def return_stroke(x):
    values = str(x).split(',')
    if len(values) > 1:
        return values[1]
    else:
        return str(x)

def return_cylinder(x):
    values = str(x).split(',')
    if len(values) > 1:
        return values[0]
    else:
        return str(x)

bikez_df['Engine stroke'] = bikez_df['Engine type'].apply(lambda x: return_stroke(x))
bikez_df['Engine cylinder'] = bikez_df['Engine type'].apply(lambda x: return_cylinder(x))
bikez_df.drop(['Engine type'], axis=1, inplace=True)

# resolve dry weight
bikez_df.loc[:, 'Dry weight (kg)'] = bikez_df['Dry weight'].str[0:5]
bikez_df['Dry weight (kg)'].replace(',', '', regex=True, inplace=True)
bikez_df['Dry weight (kg)'] = bikez_df['Dry weight (kg)'].astype(float)
bikez_df.drop(['Dry weight'], axis=1, inplace=True)

# bikez_df year to string
bikez_df.Year = bikez_df.Year.apply(lambda x: str(x).lower().strip())

# keeping only most important attributes
bikez_df = bikez_df[['Brand',
                     'Model', 
                     'Year', 
                     'Category', 
                     'Rating', 
                     'Displacement (ccm)',
                     'Power (hp)',
                     'Torque (Nm)',
                     'Engine cylinder',
                     'Engine stroke',
                     'Gearbox',
                     'Bore (mm)',
                     'Stroke (mm)',
                     'Transmission type',
                     'Front brakes', 
                     'Rear brakes',
                     'Front tire',
                     'Rear tire',
                     'Front suspension',
                     'Rear suspension',
                     'Dry weight (kg)', 
                     'Wheelbase (mm)', 
                     'Fuel capacity (lts)',
                     'Fuel system',
                     'Fuel control',
                     'Seat height (mm)',
                     'Cooling system',
                     'Color options']]

# merge bikez_df and mundimoto_df
mundimoto_df["Model and Year"] = mundimoto_df[['Model', 'Year']].agg(' '.join, axis=1)
bikez_df["Model and Year"] = bikez_df[['Model', 'Year']].agg(' '.join, axis=1)
df_final = mundimoto_df.merge(bikez_df, on='Model and Year', how='inner', indicator=True)

# merge clean-up
df_final.drop(['Brand_y', 'Model_y', 'Year_y', 'Model and Year', '_merge'], axis=1, inplace=True)
df_final.rename(columns = {'Brand_x':'Brand', 'Model_x':'Model', 'Year_x':'Year'}, inplace = True)

# send to formatted zone
df_final.to_csv('formatted/bikez_mundimoto.csv', index=False)
bikez_df.to_csv('landing/persistent/bikez_final.csv', index=False)