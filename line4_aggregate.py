# -*- coding: utf-8 -*-
"""Bead Data Visualization in Streamlit"""

import streamlit as st
import pandas as pd
import zipfile
import os
import plotly.graph_objects as go

# Set page layout to wide
st.set_page_config(layout="wide")

# Function to extract zip file
def extract_zip(uploaded_file):
    with zipfile.ZipFile(uploaded_file, 'r') as z:
        z.extractall('data')
    return 'data'

# Function to list folders
def list_folders(path):
    return sorted([f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))])

# Function to load CSV files
def load_csv_files(path):
    csv_files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.csv')]
    data = []
    for csv_file in csv_files:
        df = pd.read_csv(csv_file, header=None)
        data.append(df)
    return data

# Function to plot data with average by bead number
def plot_data(data, identifier):
    fig = go.Figure()

    for df in data:
        # Filter data for the specified identifier (e.g., Ch01, Ch02, Ch03)
        subset = df[df[0] == identifier]
        
        # Group data by Bead/Segment Number and calculate mean
        means = subset.iloc[:, 1:].mean(axis=0)  # Calculates mean across rows for each bead
        bead_numbers = list(range(1, len(means) + 1))  # Assuming bead numbers are sequential
        
        # Plot data
        fig.add_trace(go.Scatter(x=bead_numbers, y=means, mode='lines+markers', name=f'{identifier} Mean'))
    
    fig.update_layout(
        title=f'{identifier} Bead Data (Averaged)',
        xaxis_title='Bead Number',
        yaxis_title='Average Value'
    )
    st.plotly_chart(fig)

# Streamlit UI
st.title('Bead Data Visualization (Averaged by Bead Number)')

# File uploader
uploaded_file = st.file_uploader("Upload a ZIP file", type="zip")

if uploaded_file is not None:
    # Extract ZIP file
    data_dir = extract_zip(uploaded_file)
    
    # List and sort base folders
    base_folder = st.selectbox('Select Folder', list_folders(data_dir))
    
    if base_folder:
        # List and sort date folders
        date_folder = st.selectbox('Select Date', list_folders(os.path.join(data_dir, base_folder)))
        
        if date_folder:
            # Load and plot data
            data = load_csv_files(os.path.join(data_dir, base_folder, date_folder))
            for identifier in ['Ch01', 'Ch02', 'Ch03']:
                st.subheader(f'Plot for {identifier}')
                plot_data(data, identifier)
