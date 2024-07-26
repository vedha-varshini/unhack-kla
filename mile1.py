from re import sub
import pandas as pd
import numpy as np
import math

# Load data from CSV files
care_areas = pd.read_csv('CareAreas.csv', names=['id', 'x1', 'x2', 'y1', 'y2'])
metadata = pd.read_csv('metadata.csv', names=['main_field_side', 'sub_field_side'],skiprows=1)
main_field_side = metadata['main_field_side'].values[0]
sub_field_side = metadata['sub_field_side'].values[0]

area=[]
nosubarea=[]
# Calculate area
for i in range (len(care_areas)):
      a=(care_areas.iloc[0,2]-care_areas.iloc[0,1])*(care_areas.iloc[0,4]-care_areas.iloc[0,3])
      n=math.ceil(a/(sub_field_side*sub_field_side))
      area.append(a)
      nosubarea.append(n)

# Calculate main fields
main_fields = []
for i, row in care_areas.iterrows():
    x1, x2, y1, y2 = row['x1'], row['x2'], row['y1'], row['y2']
    # Calculate the required number of main fields
    main_x_steps = math.ceil((x2 - x1) / main_field_side)
    main_y_steps = math.ceil((y2 - y1) / main_field_side)
    for mx in range(main_x_steps):
        for my in range(main_y_steps):
            mf_x1 = x1 + mx * main_field_side
            mf_y1 = y1 + my * main_field_side
            mf_x2 = min(mf_x1 + main_field_side, x2)
            mf_y2 = min(mf_y1 + main_field_side, y2)
            main_fields.append([i, mf_x1, mf_x2, mf_y1, mf_y2])
# Calculate subfields
sub_fields = []
sub_field_id = 0
for main_fiel in main_fields:
    i, mf_x1, mf_x2, mf_y1, mf_y2 = main_fiel
    sub_x_steps = math.ceil((mf_x2 - mf_x1) / sub_field_side)
    sub_y_steps = math.ceil((mf_y2 - mf_y1) / sub_field_side)
    for sx in range(sub_x_steps):
        for sy in range(sub_y_steps):
            sf_x1 = mf_x1 + sx * sub_field_side
            sf_y1 = mf_y1 + sy * sub_field_side
            sf_x2 = min(sf_x1 + sub_field_side, mf_x2)
            sf_y2 = min(sf_y1 + sub_field_side, mf_y2)
            sub_fields.append([sub_field_id, sf_x1, sf_x2, sf_y1, sf_y2,i])
            sub_field_id += 1
main_field = pd.DataFrame(main_fields)
sub_fields = pd.DataFrame(sub_fields)
main_field.to_csv('mainfields.csv', index=False)
sub_fields.to_csv('subfields.csv', index=False)