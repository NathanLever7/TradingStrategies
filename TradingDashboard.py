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
st.write('''    3. We decide to invest a fixed amount for each respective strategy, which corresponds to (1/(Length of Holding Period))*100. This means for the 1 day strategy, it is an investment of 100, and a 10 day strategy has an investment of 10 each time. This is to ensure there is spare capacity for further investment.''')
st.write('''We gather the results of the different strategies, and use this to define an optimal approach.''')
st.write('''NB: The data used begins from 01/01/2022, and the end date is defined for each security.''')






# Create a dropdown menu with VUSA as an option
selected_stock = st.selectbox('Select Security:', ['VUSA (S&P 500)'])

if selected_stock == 'VUSA (S&P 500)':
  
    # Load the CSV file from the GitHub repository (use the raw URL of the CSV file)
    csv_url = 'https://raw.githubusercontent.com/NathanLever7/TradingStrategies/main/VUSA_Metrics.csv'
    data = pd.read_csv(csv_url)

    # 1. Rename the first column and update its values
    data.rename(columns={data.columns[0]: 'Days Holding Security'}, inplace=True)
    data['Days Holding'] = range(1, 11)
    
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





