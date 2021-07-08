import streamlit as st
import pandas as pd
from scipy.stats import linregress
import matplotlib.pyplot as plt

st.title('Global Sea Level App')

st.markdown("""
This app predicts the global average sea level.
* **Python libraries:** pandas, streamlit, matplotlib, scipy
* **Data source:** Global Average Absolute Sea Level Change, 1880-2014 from the US Environmental Protection Agency 
using data from CSIRO, 2015; NOAA, 2015. 
[https://datahub.io/core/sea-level-rise](https://datahub.io/core/sea-level-rise).
""")


# Load data
@st.cache
def load_data():
    return pd.read_csv('epa-sea-level.csv')


level_sea_data = load_data()

#'from-to' year selectboxes
selected_year_from  = st.sidebar.selectbox('Year from: ', level_sea_data['Year'][: -10])
selected_year_to = st.sidebar.selectbox('Predict to: ', list(range(2040, 2101)))


#predict sea level function
def get_line(year_from, df):
    df = df[df['Year'] >= year_from]
    slope, intercept, r, p, se = linregress(df['Year'], df['CSIRO Adjusted Sea Level'])
    return slope, intercept


slope, intercept = get_line(selected_year_from, level_sea_data)
predict_sea_level = slope * selected_year_to  + intercept

st.subheader(f'Predict level in {selected_year_to} (using data from {selected_year_from}):')
st.header (f'{round(predict_sea_level, 2)} inches')
st.write('')
st.write('')


#plot
predict_x = range(selected_year_from, selected_year_to)
predict_y = [slope * i + intercept for i in predict_x]

fig, ax = plt.subplots()

#plot sea level data
level_sea_data.plot(kind='scatter', x='Year', y='CSIRO Adjusted Sea Level', ax=ax)

#plot predict line
ax.plot(predict_x, predict_y, color='red', label=f'data from {selected_year_from}')

#plot predict line (all_period)
start = level_sea_data.loc[0, 'Year']
all_slope, all_intercept = get_line(start, level_sea_data)
all_x = range(start, selected_year_to)
all_y = [all_slope * i + all_intercept for i in all_x]
ax.plot(all_x, all_y, color='green', label=f'data from {start}')
plt.title('Rise in Sea Level')
plt.ylabel('Sea Level (inches)')
ax.legend()
st.write(fig)


#plot predict level changing
fig, ax = plt.subplots()

y_pred = []
start_year = level_sea_data.loc[0, 'Year']
for year in range(start_year, selected_year_from):
    y_slope, y_intercept = get_line(year, level_sea_data)
    y_pred.append(y_slope * selected_year_to + y_intercept)

x = list(range(start_year, selected_year_from))
ax.plot(x, y_pred, color='green')
plt.title('Predicted Sea Level Change')
plt.ylabel(f'Predicted Sea Level in {selected_year_to} (inches)')
plt.xlabel(f'Using data from (year)')
st.write(fig)