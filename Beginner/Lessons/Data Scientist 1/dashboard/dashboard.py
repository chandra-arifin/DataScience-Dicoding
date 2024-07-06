import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_daily_rent_df(df):
    daily_rent_df = df.resample(rule='D', on='dteday_x').agg({
        "instant": "nunique",
        "cnt_x": "sum"
    })
    daily_rent_df = daily_rent_df.reset_index()
    daily_rent_df.rename(columns={
        "instant": "jml_jam",
        "cnt_x": "jml_pemakai"
    }, inplace=True)
        
    return daily_rent_df

def create_month_rent_df(df):
    month_rent_df = df.groupby(by=["yr_x", "mnth_x"]).cnt_x.sum().reset_index()
    month_rent_df.rename(columns={
        "instant": "jml_jam",
        "cnt_x": "jml_pemakai"
    }, inplace=True)
        
    return month_rent_df

def create_byseason_df(df):
    byseason_df = df.groupby(by="season_x").cnt_x.sum().reset_index()
    byseason_df.rename(columns={
        "instant": "jml_jam"
    }, inplace=True)
        
    return byseason_df
def create_weathersit_df(df):
    weathersit_df = df.groupby(by="weathersit_x").cnt_x.sum().reset_index()
    weathersit_df.rename(columns={
        "instant": "jml_jam"
    }, inplace=True)
        
    return weathersit_df

def create_byholiday_df(df):
    byholiday_df = df.groupby(by="holiday_x").cnt_x.sum().reset_index()
    byholiday_df.rename(columns={
        "cnt_x": "jml_pemakai"
    }, inplace=True)
        
    return byholiday_df

def create_byweekday_df(df):
    byweekday_df = df.groupby(by="weekday_x").cnt_x.sum().reset_index()
    byweekday_df.rename(columns={
        "cnt_x": "jml_pemakai"
    }, inplace=True)
    byweekday_df['weekday_x'] = pd.Categorical(byweekday_df['weekday_x'], ["Sunday", "Monday", "Tuesday", "Wenesday", "Thursday", "Friday", "Saturday"])

    return byweekday_df

def create_workingday_df(df):
    workingday_df = df.groupby(by="workingday_x").cnt_x.sum().reset_index()
    workingday_df.rename(columns={
        "cnt_x": "jml_pemakai"
    }, inplace=True)
        
    return workingday_df

def create_bytemp_df(df):
    bytemp_df = df.groupby(by="temp_group_y").cnt_y.sum().reset_index()
    bytemp_df.rename(columns={
        "cnt_y": "jml_pemakai"
    }, inplace=True)
    bytemp_df['temp_group_y'] = pd.Categorical(bytemp_df['temp_group_y'], ["Low_Temp", "Normal_Temp", "High_Temp"])
        
    return bytemp_df

def create_byatemp_df(df):
    byatemp_df = df.groupby(by="atemp_group_y").cnt_y.sum().reset_index()
    byatemp_df.rename(columns={
        "cnt_y": "jml_pemakai"
    }, inplace=True)
    byatemp_df['atemp_group_y'] = pd.Categorical(byatemp_df['atemp_group_y'], ["Low_Atemp", "Normal_Atemp", "High_Atemp"])
        
    return byatemp_df

def create_hum_df(df):
    hum_df = df.groupby(by="hum_group_y").cnt_y.sum().reset_index()
    hum_df.rename(columns={
        "cnt_y": "jml_pemakai"
    }, inplace=True)
    hum_df['hum_group_y'] = pd.Categorical(hum_df['hum_group_y'], ["Low_Hum", "Normal_Hum", "High_Hum"])
        
    return hum_df

def create_bywindspeed_df(df):
    bywindspeed_df = df.groupby(by="windspeed_group_y").cnt_y.sum().reset_index()
    bywindspeed_df.rename(columns={
        "cnt_y": "jml_pemakai"
    }, inplace=True)
    bywindspeed_df['windspeed_group_y'] = pd.Categorical(bywindspeed_df['windspeed_group_y'], ["Low_windspeed", "Normal_windspeed", "High_windspeed"])
        
    return bywindspeed_df

def create_byhour_df(df):
    byhour_df = df.groupby(by="hr_group").cnt_y.sum().reset_index()
    byhour_df.rename(columns={
        "cnt_y": "jml_pemakai"
    }, inplace=True)
    byhour_df['hr_group'] = pd.Categorical(byhour_df['hr_group'], ["Morning", "Noon", "Afternoon", "Night"])
        
    return byhour_df

def create_rfm_df(df):
    rfm_df = df.groupby(by="instant", as_index=False).agg({
        "dteday_x": "max", #mengambil tanggal order terakhir
        "cnt_x": "sum"
    })
    rfm_df.columns = ["instant", "max_rent_timestamp", "monetary"]
        
    rfm_df["max_rent_timestamp"] = rfm_df["max_rent_timestamp"].dt.date
    recent_date = df["dteday_x"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_rent_timestamp"].apply(lambda x: (recent_date - x).days)
    rfm_df.drop("max_rent_timestamp", axis=1, inplace=True)
        
    return rfm_df

all_df = pd.read_csv("all_data.csv")

datetime_columns = ["dteday_x", "dteday_y"]
all_df.sort_values(by="dteday_x", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])
    
min_date = all_df["dteday_x"].min()
max_date = all_df["dteday_x"].max()
    
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
        
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
main_df = all_df[(all_df["dteday_x"] >= str(start_date)) & 
                (all_df["dteday_x"] <= str(end_date))]

daily_rent_df = create_daily_rent_df(main_df)
month_rent_df = create_month_rent_df(main_df)
byseason_df = create_byseason_df(main_df)
byholiday_df = create_byholiday_df(main_df)
byweekday_df = create_byweekday_df(main_df)
workingday_df = create_workingday_df(main_df)
weathersit_df = create_weathersit_df(main_df)
bytemp_df = create_bytemp_df(main_df)
byatemp_df = create_byatemp_df(main_df)
hum_df = create_hum_df(main_df)
bywindspeed_df = create_bywindspeed_df(main_df)
byhour_df = create_byhour_df(main_df)
rfm_df = create_rfm_df(main_df)

st.header('Rent Bike Dashboard :sparkles:')

st.subheader('Total Rent')

col1, col2, col3 = st.columns(3)

with col1:
    total_rent = daily_rent_df.jml_pemakai.sum()
    st.metric("Total Rent", value=total_rent)

with col2:
    total_hours = daily_rent_df.jml_jam.count()
    st.metric("Total Hari", value=total_hours)
    
with col3:
    total_rentdays = round(daily_rent_df.jml_pemakai.sum() / daily_rent_df.jml_jam.count(), 2)
    st.metric("Total Per Hari", value=total_rentdays)
    
st.subheader("Jumlah Pemakai Sepeda Dari Bulan Ke Bulan")

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    month_rent_df["mnth_x"],
    month_rent_df["jml_pemakai"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)


st.subheader("Berdasarkan Musim & Cuaca Menggunakan Sepeda")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

# sns.barplot(x="cnt_x", y="season_x", data=byseason_df.head(5), palette=colors, ax=ax[0])
sns.barplot(x="cnt_x", y="season_x", data=byseason_df.sort_values(by="cnt_x", ascending=False).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Jumlah Pemakai", fontsize=30)
ax[0].set_title("Number of Rent by Season", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x="cnt_x", y="weathersit_x", data=weathersit_df.sort_values(by="cnt_x", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Jumlah Pemakai", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Number of Rent by Weathersit", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
    
st.pyplot(fig)

st.subheader("Jam, Hari Kerja, Hari Libur & Nama Hari Terbanyak Penggunaan Sepeda")

col1, col2, col3 = st.columns(3)

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    colors = ["#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3"]

    sns.barplot(
        y="jml_pemakai", 
        x="hr_group",
        data=byhour_df.sort_values(by="hr_group", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Rent by Hours", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
    
with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
        
    colors = ["#90CAF9", "#D3D3D3"]
    
    sns.barplot(
        y="jml_pemakai", 
        x="workingday_x",
        data=workingday_df.sort_values(by="workingday_x", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Rent by Working Day", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
    
with col3:
    fig, ax = plt.subplots(figsize=(20, 10))
        
    colors = ["#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    
    sns.barplot(
        y="jml_pemakai", 
        x="holiday_x",
        data=byholiday_df.sort_values(by="holiday_x", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Rent by Holiday", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
    
fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3"]
sns.barplot(
    y="jml_pemakai", 
    x="weekday_x",
    data=byweekday_df.sort_values(by="weekday_x", ascending=True),
    palette=colors,
    ax=ax
)
ax.set_title("Number of Rent by Weekday", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

st.subheader("Penggunaan Sepeda Berdasarkan Temperatur, Atemperatur, Humidity dan Windspeed")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3"]

    sns.barplot(
        y="jml_pemakai", 
        x="temp_group_y",
        data=bytemp_df.sort_values(by="temp_group_y", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Rent by Temp", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
    
with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3"]

    sns.barplot(
        y="jml_pemakai", 
        x="atemp_group_y",
        data=byatemp_df.sort_values(by="atemp_group_y", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Rent by Atemp", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
    
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    colors = ["#D3D3D3", "#90CAF9", "#D3D3D3"]

    sns.barplot(
        y="jml_pemakai", 
        x="hum_group_y",
        data=hum_df.sort_values(by="hum_group_y", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Rent by Humidity", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
    
with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3"]

    sns.barplot(
        y="jml_pemakai", 
        x="windspeed_group_y",
        data=bywindspeed_df.sort_values(by="windspeed_group_y", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Rent by Windspeed", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)