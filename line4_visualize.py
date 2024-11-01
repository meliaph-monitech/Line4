# -*- coding: utf-8 -*-
"""Untitled6.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1nxLbYE15VCIfpR5z_apPUV0x8_EMEPQN
"""

import streamlit as st
import pandas as pd
import zipfile
import os
import matplotlib.pyplot as plt
from io import BytesIO

# Function to extract zip file
def extract_zip(uploaded_file):
    with zipfile.ZipFile(uploaded_file, 'r') as z:
        z.extractall('data')
    return 'data'

# Function to list folders
def list_folders(path):
    return [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

# Function to load CSV files
def load_csv_files(path):
    csv_files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.csv')]
    data = []
    for csv_file in csv_files:
        df = pd.read_csv(csv_file, header=None)
        data.append(df)
    return data

# Function to plot data
def plot_data(data, identifier):
    plt.figure(figsize=(10, 6))
    for df in data:
        subset = df[df[0] == identifier]
        values = subset.iloc[:, 1:].values.flatten()
        plt.plot(values, label=f'{identifier}')
    plt.title(f'{identifier} Bead Data')
    plt.xlabel('Measurement')
    plt.ylabel('Value')
    plt.legend()
    st.pyplot(plt)

# Streamlit UI
st.title('Bead Data Visualization')

# File uploader
uploaded_file = st.file_uploader("Upload a ZIP file", type="zip")

if uploaded_file is not None:
    # Extract ZIP file
    data_dir = extract_zip(uploaded_file)

    # List base folders
    base_folder = st.selectbox('Select Folder', list_folders(data_dir))

    if base_folder:
        # List date folders
        date_folder = st.selectbox('Select Date', list_folders(os.path.join(data_dir, base_folder)))

        if date_folder:
            # Load and plot data
            data = load_csv_files(os.path.join(data_dir, base_folder, date_folder))
            for identifier in ['Ch01', 'Ch02', 'Ch03']:
                st.subheader(f'Plot for {identifier}')
                plot_data(data, identifier)