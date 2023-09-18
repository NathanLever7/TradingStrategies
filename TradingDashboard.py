import streamlit as st
import pandas as pd

# Set the title of the streamlit dashboard
st.title('Index Trading Strategies')

# Create a dropdown menu with VUSA as an option
selected_stock = st.selectbox('Select Stock:', ['VUSA (S&P 500)'])

if selected_stock == 'VUSA (S&P 500)':
  
    # Load the CSV file from the GitHub repository (use the raw URL of the CSV file)
    csv_url = 'https://raw.githubusercontent.com/NathanLever7/TradingStrategies/main/VUSA_Metrics.csv'
    data = pd.read_csv(csv_url)

    # 1. Rename the first column and update its values
    data.rename(columns={data.columns[0]: 'Days Holding Security'}, inplace=True)
    data['Days Holding Security'] = range(1, 11)
    
    # 2. Remove the Average_RMSE column
    data.drop(columns=['Average_RMSE'], inplace=True)
    
    # 3. Move the Average_MAE column to the end and rename it
    average_mae = data.pop('Average_MAE')
    data['Average MAE'] = average_mae
    
    # 4. Remove the specified columns
    data.drop(columns=['Average_Actual_Return_Positive', 'Average_Actual_Return_Negative'], inplace=True)

    # 5. Rename a column and round its values to 3 decimal places, then add a % sign
    data.rename(columns={'Average_Actual_Return_Positive_Daily': 'Actual Daily Return when Buying after Positive Prediction'}, inplace=True)
    data['Actual Daily Return when Buying after Positive Prediction'] = data['Actual Daily Return when Buying after Positive Prediction'].astype(float).round(3).astype(str) + '%'

    # 6. Do the equivalent for another column
    data.rename(columns={'Average_Actual_Return_Negative_Daily': 'Actual Daily Return when Buying after Negative Prediction'}, inplace=True)
    data['Actual Daily Return when Buying after Negative Prediction'] = data['Actual Daily Return when Buying after Negative Prediction'].astype(float).round(3).astype(str) + '%'

    # 7. Rename two more columns
    data.rename(columns={'Capital_Positive': 'Capital following Positive Prediction Strategy', 
                         'Capital_Negative': 'Capital following Negative Prediction Strategy'}, inplace=True)
    
    # 8. Rename another column
    data.rename(columns={'Capital_Daily_Investment': 'Capital Investing Every Day'}, inplace=True)
    
    # 9. Remove the Time_Taken column
    data.drop(columns=['Time_Taken'], inplace=True)

    # Round all numerical values to 3 decimal places
    for col in data.select_dtypes(include=['float64']).columns:
        data[col] = data[col].round(3)
    
    # Print the modified DataFrame on the streamlit web page
    st.write(data)





