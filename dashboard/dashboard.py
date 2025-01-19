import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set_theme(style='dark')

df = pd.read_csv('main_data.csv')
df['dteday'] = pd.to_datetime(df['dteday'])

def create_monthly_df(df):
    monthly_df = df.resample(rule="ME", on="dteday").agg(
        {"registered": "sum", "cnt": "sum"}
    )
    monthly_df.index = monthly_df.index.strftime("%Y-%m")
    monthly_df = monthly_df.reset_index()
    monthly_df.rename(columns={"dteday": "month"}, inplace=True)
    return monthly_df

def create_by_season_df(df):
    day_df_by_season = df.groupby(by="season").agg(
        {"casual": "sum", "registered": "sum", "cnt": "sum"}
    )
    mapping = {1: "Springer", 2: "Summer", 3: "Fall", 4: "Winter"}
    day_df_by_season.index = day_df_by_season.index.map(mapping)
    day_df_by_season = day_df_by_season.reset_index()
    return day_df_by_season

with st.sidebar:
    st.image('https://www.jamesdunloptextiles.com/cdn-cgi/image/fit=cover,width=220,height=220,format=auto/https://media.jamesdunloptextiles.com/media/uploads/2018_08/CASAMANCE_38290798.jpg')

    start_date, end_date = st.date_input(
        label='Rentang waktu',
        min_value=pd.to_datetime("2011-01-01"),
        max_value=pd.to_datetime("2012-12-31"),
        value=[pd.to_datetime("2011-01-01"), pd.to_datetime("2012-12-31")]
    )

main_df = df[(df['dteday'] >= str(start_date)) &
                 (df['dteday'] <= str(end_date))]

start_year = start_date.strftime('%Y')
end_year = end_date.strftime('%Y')

st.subheader(f'Number of Rent per Day')
tab1, tab2, tab3 = st.tabs(["Casual", "Registered", "Mix"])

with tab1:
    minimum_casual = main_df.iloc[main_df.casual.idxmin()]['casual'].item()
    maximum_casual = main_df.iloc[main_df.casual.idxmax()]['casual'].item()
    minimum_casual_date = main_df.iloc[main_df.casual.idxmin()]['dteday']
    maximum_casual_date = main_df.iloc[main_df.casual.idxmax()]['dteday']

    fig, ax = plt.subplots(figsize=(18, 3))
    ax.plot(main_df["dteday"], main_df["casual"], linewidth=2)
    ax.scatter(
        maximum_casual_date,
        maximum_casual,
        color="red",
    )
    ax.text(
        maximum_casual_date,
        maximum_casual,
        f"Peak: {maximum_casual} @ {maximum_casual_date.strftime('%Y-%m-%d')}",
        color="red",
        fontsize=15,
        ha="center",
    )
    ax.scatter(
        minimum_casual_date,
        minimum_casual,
        color="red",
    )
    ax.text(
        minimum_casual_date,
        minimum_casual,
        f"Minimum: {minimum_casual} @ {minimum_casual_date.strftime('%Y-%m-%d')}",
        color="red",
        fontsize=15,
        ha="center",
    )
    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=10)
    st.pyplot(fig)

with tab2:
    minimum_registered = main_df.iloc[main_df.registered.idxmin()]['registered'].item()
    maximum_registered = main_df.iloc[main_df.registered.idxmax()]['registered'].item()
    minimum_registered_date = main_df.iloc[main_df.registered.idxmin()]['dteday']
    maximum_registered_date = main_df.iloc[main_df.registered.idxmax()]['dteday']

    fig, ax = plt.subplots(figsize=(18, 3))
    ax.plot(main_df["dteday"], main_df["registered"], linewidth=2)
    ax.scatter(
        maximum_registered_date,
        maximum_registered,
        color="red",
    )
    ax.text(
        maximum_registered_date,
        maximum_registered,
        f"Peak: {maximum_registered} @ {maximum_registered_date.strftime('%Y-%m-%d')}",
        color="red",
        fontsize=15,
        ha="center",
    )
    ax.scatter(
        minimum_registered_date,
        minimum_registered,
        color="red",
    )
    ax.text(
        minimum_registered_date,
        minimum_registered,
        f"Minimum: {minimum_registered} @ {minimum_registered_date.strftime('%Y-%m-%d')}",
        color="red",
        fontsize=15,
        ha="center",
    )
    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=10)
    st.pyplot(fig)

with tab3:
    minimum_cnt = main_df.iloc[main_df.cnt.idxmin()]['cnt'].item()
    maximum_cnt = main_df.iloc[main_df.cnt.idxmax()]['cnt'].item()
    minimum_cnt_date = main_df.iloc[main_df.cnt.idxmin()]['dteday']
    maximum_cnt_date = main_df.iloc[main_df.cnt.idxmax()]['dteday']

    fig, ax = plt.subplots(figsize=(18, 3))
    ax.plot(main_df["dteday"], main_df["cnt"], linewidth=2)
    ax.scatter(
        maximum_cnt_date,
        maximum_cnt,
        color="red",
    )
    ax.text(
        maximum_cnt_date,
        maximum_cnt,
        f"Peak: {maximum_cnt} @ {maximum_cnt_date.strftime('%Y-%m-%d')}",
        color="red",
        fontsize=15,
        ha="center",
    )
    ax.scatter(
        minimum_cnt_date,
        minimum_cnt,
        color="red",
    )
    ax.text(
        minimum_cnt_date,
        minimum_cnt,
        f"Minimum: {minimum_cnt} @ {minimum_cnt_date.strftime('%Y-%m-%d')}",
        color="red",
        fontsize=15,
        ha="center",
    )
    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=10)
    st.pyplot(fig)

st.subheader(f'Rent Number by Season')
by_season_df = create_by_season_df(main_df)
fig, ax = plt.subplots(figsize=(8, 3))
sns.barplot(
    x="season",
    y="cnt",
    data=by_season_df,
    ax=ax,
)
ax.set_ylabel("Number of rent (in hundred of thousands)", fontsize=8)
ax.set_xlabel(None)
ax.set_yticks(np.arange(0, 1_200_000, 100_000))
ax.tick_params(axis="y", labelsize=6)
ax.tick_params(axis="x", labelsize=8)
st.pyplot(fig)

col1, col2 = st.columns(2)

with col1:
    st.subheader('Number of rent (cnt) vs Temperature (temp)')
    fig, ax = plt.subplots()
    ax.scatter(main_df["cnt"], main_df["temp"])
    ax.set_xlabel('cnt')
    ax.set_ylabel('temp (normalized to 41°C)')
    fig.suptitle(f"Correlation = {round(main_df.corr()[['temp', 'atemp', 'hum', 'windspeed']].iloc[-1]['temp'], 2)}", y=0.93, fontsize=12)
    st.pyplot(fig)

    st.subheader('Number of rent (cnt) vs Feeling Temperature (atemp)')
    fig, ax = plt.subplots()
    ax.scatter(main_df["cnt"], main_df["atemp"])
    ax.set_xlabel('cnt')
    ax.set_ylabel('atemp (normalized to 50°C)')
    fig.suptitle(f"Correlation = {round(main_df.corr()[['temp', 'atemp', 'hum', 'windspeed']].iloc[-1]['atemp'], 2)}", y=0.93, fontsize=12)
    st.pyplot(fig)

with col2:
    st.subheader('Number of rent (cnt) vs Humidity (hum)')
    fig, ax = plt.subplots()
    ax.scatter(main_df["cnt"], main_df["hum"])
    ax.set_xlabel('cnt')
    ax.set_ylabel('hum (normalized to 100)')
    fig.suptitle(f"Correlation = {round(main_df.corr()[['temp', 'atemp', 'hum', 'windspeed']].iloc[-1]['hum'], 2)}", y=0.93, fontsize=12)
    st.pyplot(fig)

    st.subheader('Number of rent (cnt) vs Windspeed (windspeed)')
    fig, ax = plt.subplots()
    ax.scatter(main_df["cnt"], main_df["windspeed"])
    ax.set_xlabel('cnt')
    ax.set_ylabel('windspeed (normalized to 67)')
    fig.suptitle(f"Correlation = {round(main_df.corr()[['temp', 'atemp', 'hum', 'windspeed']].iloc[-1]['windspeed'], 2)}", y=0.93, fontsize=12)
    st.pyplot(fig)

st.caption('Made with 💗 by A. Fauzan Adhima')