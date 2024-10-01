import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='darkgrid')

# Menghitung total penggunaan sepeda berdasarkan 'workingday_day'
def calculate_daily_usage(df):
    if df.empty:
        return pd.DataFrame()  # Mengembalikan dataframe kosong jika data tidak ada
    daily_usage = df.groupby('workingday_day')['cnt_day'].sum().reset_index()
    return daily_usage

# Membuat visualisasi total penggunaan sepeda berdasarkan 'workingday_day'
def plot_daily_usage(daily_usage_df):
    if daily_usage_df.empty:
        st.warning('Tidak ada data yang sesuai untuk ditampilkan pada grafik penggunaan harian.')
        return
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=daily_usage_df, x='workingday_day', y='cnt_day', palette='pastel', ax=ax)
    ax.set_title('Total Penggunaan Sepeda: Hari Kerja vs Akhir Pekan')
    ax.set_xlabel('Hari Kerja (1 = Ya, 0 = Tidak)')
    ax.set_ylabel('Total Penggunaan Sepeda')
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Akhir Pekan', 'Hari Kerja'])
    ax.grid(axis='y')
    st.pyplot(fig)

# Menambahkan kolom 'day_type'
def add_day_type(df):
    df['day_type'] = df['workingday_day'].map({0: 'Akhir Pekan', 1: 'Hari Kerja'})
    return df

# Menghitung rata-rata penggunaan sepeda per jam berdasarkan tipe hari
def calculate_hourly_usage(df):
    if df.empty:
        return pd.DataFrame()  # Mengembalikan dataframe kosong jika data tidak ada
    hourly_usage = df.groupby(['weekday_hour', 'day_type'])['cnt_hour'].mean().reset_index()
    return hourly_usage

# Membuat visualisasi rata-rata penggunaan sepeda per jam
def plot_hourly_usage(hourly_usage_df):
    if hourly_usage_df.empty:
        st.warning('Tidak ada data yang sesuai untuk ditampilkan pada grafik penggunaan per jam.')
        return
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=hourly_usage_df, x='weekday_hour', y='cnt_hour', hue='day_type', marker='o', palette='Set1', ax=ax)
    ax.set_title('Pola Penggunaan Sepeda Per Jam: Hari Kerja vs Akhir Pekan')
    ax.set_xlabel('Jam')
    ax.set_ylabel('Rata-rata Penggunaan Sepeda')
    ax.set_xticks(range(0, 12))
    ax.grid(True)
    st.pyplot(fig)

# Membuat visualisasi scatter plot pengaruh suhu terhadap jumlah pengguna sepeda
def plot_scatter_temp_vs_cnt(df):
    if df.empty:
        st.warning('Tidak ada data yang sesuai untuk scatter plot.')
        return
    palette = {'Akhir Pekan': 'blue', 'Hari Kerja': 'orange'}
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.scatterplot(data=df, x='temp_hour', y='cnt_hour', hue='day_type', palette=palette, alpha=0.6, ax=ax)
    ax.set_title('Pengaruh Suhu Terhadap Jumlah Pengguna Sepeda')
    ax.set_xlabel('Suhu (temp_hour)')
    ax.set_ylabel('Jumlah Pengguna Sepeda (cnt_hour)')
    ax.grid(True)
    st.pyplot(fig)

# Membuat visualisasi distribusi jumlah pengguna sepeda berdasarkan cuaca
def plot_box_weather_vs_cnt(df):
    if df.empty:
        st.warning('Tidak ada data yang sesuai untuk box plot.')
        return
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(data=df, x='weathersit_day', y='cnt_hour', hue='day_type', palette='Set2', ax=ax)
    ax.set_title('Distribusi Jumlah Pengguna Sepeda Berdasarkan Cuaca')
    ax.set_xlabel('Kategori Cuaca (1 = Clear, 2 = Misty, 3 = Light Rain, 4 = Heavy Rain)')
    ax.set_ylabel('Jumlah Pengguna Sepeda (cnt_hour)')
    ax.grid(True)
    st.pyplot(fig)

# Load data
combined_data = pd.read_csv('combined_data.csv')

# Menggunakan 'dteday' untuk filter harian
combined_data['dteday'] = pd.to_datetime(combined_data['dteday'])

# Pastikan data memiliki nilai minimum dan maksimum
if combined_data['dteday'].empty:
    st.error("Data 'dteday' tidak ditemukan.")
else:
    min_day = combined_data['dteday'].min()
    max_day = combined_data['dteday'].max()

with st.sidebar:
    st.image("https://www.brandcrowd.com/blog/wp-content/uploads/2019/06/bike-share.png")
    
    # Date filter menggunakan 'dteday'
    if not combined_data.empty:
        start_day, end_day = st.date_input('Rentang Hari', [min_day, max_day], min_value=min_day, max_value=max_day)

# Filter data berdasarkan 'dteday'
filtered_data = combined_data[(combined_data['dteday'] >= pd.to_datetime(start_day)) & 
                              (combined_data['dteday'] <= pd.to_datetime(end_day))]

# Menambahkan kolom 'day_type'
filtered_data = add_day_type(filtered_data)

# Pastikan data tidak kosong sebelum visualisasi
if not filtered_data.empty:
    # Total penggunaan sepeda berdasarkan hari kerja vs akhir pekan
    daily_usage_df = calculate_daily_usage(filtered_data)
    plot_daily_usage(daily_usage_df)

    # Rata-rata penggunaan sepeda per jam
    hourly_usage_df = calculate_hourly_usage(filtered_data)
    plot_hourly_usage(hourly_usage_df)

    # Scatter plot pengaruh suhu terhadap jumlah pengguna sepeda
    plot_scatter_temp_vs_cnt(filtered_data)

    # Distribusi jumlah pengguna sepeda berdasarkan cuaca
    plot_box_weather_vs_cnt(filtered_data)
else:
    st.warning('Tidak ada data yang sesuai dengan filter yang dipilih.')

