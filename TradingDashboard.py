import streamlit as st
import pandas as pd

# Set the title of the streamlit dashboard
st.title('Index Trading Strategies')

# Add a subheading
st.subheader('Choosing Optimal Strategies for Each Security')

# Add descriptive text under the subheading
st.write('''When choosing our investments, we wish to run models on multiple different securities, judging their profitability over different time horizons. However, this is computationally expensive. In this section, we look at each security and define the optimal time horizon. This optimal time horizon is what we will use when running our models for investment suggestions each day.''')
st.write('''Each dataframe has information on the per day returns for each holding length strategy, and contrasts results when investing when predictions are positive, negative, and regardless of prediction. This shows the performance of our algorithm.''')
st.write('''Each dataframe also has the overall capital when following an investment strategy that is as follows:''')
st.write('''    1. Our given starting capital is 100.''')
st.write('''    2. Invest according to the strategy (whether predictions are positive, negative or irrespective of the prediction).''')
st.write('''    3. We decide to invest a fixed amount for each respective strategy, which corresponds to (1/(Length of Holding Period))*100. This means that the 1 day strategy has an investment of 100 each time, whilst the 10 day strategy has an investment of 10 each time. This is to ensure there is spare capacity for further investment, if required.''')
st.write('''We gather the results of the different strategies, and use this to define an optimal approach.''')
st.write('''NB: The data used begins from 01/01/2022, and the end date is defined for each security.''')



def load_and_preprocess_data(csv_url):
  data = pd.read_csv(csv_url)  
  
  # 1. Rename the first column and update its values
  data.rename(columns={data.columns[0]: 'Days Holding'}, inplace=True)
  data['Days Holding'] = range(1, 11)
  
  # 2. Remove the Average_RMSE column
  data.drop(columns=['Average_RMSE'], inplace=True)
  
  # 3. Move the Average_MAE column to the end and rename it
  average_mae = data.pop('Average_MAE')
  data['Average MAE'] = average_mae
  
  # 4. Remove the specified columns
  data.drop(columns=['Average_Actual_Return_Positive', 'Average_Actual_Return_Negative'], inplace=True)

  # 5. Rename a column and round its values to 3 decimal places, then add a % sign
  data.rename(columns={'Average_Actual_Return_Positive_Daily': 'Daily Return with Positive Prediction Strategy'}, inplace=True)
  data['Daily Return with Positive Prediction Strategy'] = data['Daily Return with Positive Prediction Strategy'].astype(float).round(3).astype(str) + '%'

  # 6. Do the equivalent for another column
  data.rename(columns={'Average_Actual_Return_Negative_Daily': 'Daily Return with Negative Prediction Strategy'}, inplace=True)
  data['Daily Return with Negative Prediction Strategy'] = data['Daily Return with Negative Prediction Strategy'].astype(float).round(3).astype(str) + '%'

  # 7. Rename two more columns
  data.rename(columns={'Capital_Positive': 'Capital with Positive Prediction Strategy', 
                       'Capital_Negative': 'Capital with Negative Prediction Strategy'}, inplace=True)
  
  # 8. Rename another column
  data.rename(columns={'Capital_Daily_Investment': 'Capital Investing Every Day'}, inplace=True)
  
  # 9. Remove the Time_Taken column
  data.drop(columns=['Time_Taken'], inplace=True)

  # 10. Round all numerical values to 3 decimal places
  for col in data.select_dtypes(include=['float64']).columns:
      data[col] = data[col].round(3)


  return data

selected_stock = st.selectbox('Select Security:', ['VUSA (S&P 500)', 'VUKE (FTSE 100)', 'INRG (iShares Global Clean Energy)', 'VUKG (FTSE 100 Growth)'])

if selected_stock == 'VUSA (S&P 500)':
    st.markdown("<small>Description for VUSA (S&P 500)</small>", unsafe_allow_html=True)
    csv_url = 'https://raw.githubusercontent.com/NathanLever7/TradingStrategies/main/VUSA_Metrics.csv'
    data = load_and_preprocess_data(csv_url)
    
    # Highlight the 3rd row
    styled = data.style.apply(lambda x: ['background: lightgreen' if x.name == 2 else '' for i in x], axis=1)\
             .set_properties(**{'width': '100px', 'text-align': 'center'})\
             .set_table_styles([dict(selector='th', props=[('max-width', '80px'), 
                                                           ('text-align', 'center'), 
                                                           ('transform', 'rotateX(45deg)'), 
                                                           ('height', '60px')])])
    st.markdown(styled.to_html(), unsafe_allow_html=True)

elif selected_stock == 'VUKE (FTSE 100)':
    csv_url = 'https://raw.githubusercontent.com/NathanLever7/TradingStrategies/main/VUKE_Metrics.csv' # Replace with the actual URL for the INRG data file
    data = load_and_preprocess_data(csv_url)
    st.write(data)
    st.write("Description for FTSE 100")
elif selected_stock == 'INRG (iShares Global Clean Energy)':
    csv_url = 'https://raw.githubusercontent.com/NathanLever7/TradingStrategies/main/INRG_Metrics.csv' # Replace with the actual URL for the INRG data file
    data = load_and_preprocess_data(csv_url)
    st.write(data)
    st.write("Description for INRG (iShares Global Clean Energy)")
elif selected_stock == 'VUKG (FTSE 100 Growth)':
    csv_url = 'https://raw.githubusercontent.com/NathanLever7/TradingStrategies/main/VUKG_Metrics.csv' # Replace with the actual URL for the VUKG data file
    data = load_and_preprocess_data(csv_url)
    st.write(data)
    st.write("Description for VUKG (FTSE 100)") # Add your description here







 
