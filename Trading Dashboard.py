import streamlit as st
import pandas as pd

# Set the title of the streamlit dashboard
st.title('Index Trading Strategies')

# Load the CSV file from the GitHub repository (use the raw URL of the CSV file)
csv_url = 'https://raw.githubusercontent.com/NathanLever7/TradingStrategies/main/VUSA_Metrics.csv'
data = pd.read_csv(csv_url)

# Print the DataFrame on the streamlit web page
st.write(data)




