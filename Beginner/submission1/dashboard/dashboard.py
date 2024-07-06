import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')


def create_tahun_registered_df(df):
    tahun_registered_df = all_df.groupby("yr").registered.sum().reset_index()
    return tahun_registered_df

def create_tahun_casual_df(df):
    tahun_casual_df = all_df.groupby("yr").casual.sum().reset_index()
    return tahun_casual_df

def create_tahun_season_df(df):
    tahun_season_df = all_df.groupby("season_name").cnt.sum().sort_values(ascending=False).reset_index()
    return tahun_season_df

all_df = pd.read_csv("main_data.csv")


all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)
 
all_df["dteday"] = pd.to_datetime(all_df["dteday"])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & (all_df["dteday"] <= str(end_date))]

tahun_registered_df = create_tahun_registered_df(main_df)
tahun_casual_df = create_tahun_casual_df(main_df)
tahun_season_df = create_tahun_season_df(main_df)

st.header(':sparkles: Bike Hiring Dashboard :sparkles:')

st.subheader("Bike Hiring Registered and Casual")
 
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
colors = ["#D3D3D3", "#90CAF9"]
 
sns.barplot(x="yr", y="registered", data=tahun_registered_df.head(), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Tahun", fontsize=30)
ax[0].set_title("Bike Hiring (Registered)", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="yr", y="casual", data=tahun_casual_df.head(), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Tahun", fontsize=30)
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Bike Hiring (Casual)", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
 
st.pyplot(fig)

st.subheader('Hiring By Season')

fig, ax = plt.subplots(figsize=(20, 10))
    
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    y="cnt", 
    x="season_name",
    data=tahun_season_df.sort_values(by="cnt", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

#apakah perlu ditampilkan semua data RAW nya...
#st.dataframe(main_df)
st.table(tahun_registered_df.iloc[0:10])
st.table(tahun_casual_df.iloc[0:10])
st.table(tahun_season_df.iloc[0:10])

st.caption('Copyright (c) Dicoding 2023')


