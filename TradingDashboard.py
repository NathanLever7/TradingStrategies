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

optimal_strategies = []

def get_optimal_strategy(data, security_name):
    optimal_row = data.iloc[[6]] if security_name != 'VUKE (FTSE 100)' and security_name != 'VUKG (FTSE 100 Growth)' else data.iloc[[4]]
    optimal_row['Security'] = security_name
    return optimal_row

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

csv_url_VUSA = 'https://raw.githubusercontent.com/NathanLever7/TradingStrategies/main/VUSA_Metrics.csv'
csv_url_VUKE = 'https://raw.githubusercontent.com/NathanLever7/TradingStrategies/main/VUKE_Metrics.csv'
csv_url_INRG = 'https://raw.githubusercontent.com/NathanLever7/TradingStrategies/main/INRG_Metrics.csv'
csv_url_VUKG = 'https://raw.githubusercontent.com/NathanLever7/TradingStrategies/main/VUKG_Metrics.csv'

data_VUSA = load_and_preprocess_data(csv_url_VUSA)
data_VUKE = load_and_preprocess_data(csv_url_VUKE)
data_INRG = load_and_preprocess_data(csv_url_INRG)
data_VUKG = load_and_preprocess_data(csv_url_VUKG)

styled_VUSA = data_VUSA.style.apply(lambda x: ['background: lightgreen' if x.name == 6 else '' for i in x], axis=1)\
             .set_properties(**{'width': '100px', 'text-align': 'center', 'font-size': '10pt'})\
             .set_table_styles([dict(selector='th', props=[('max-width', '80px'), 
                                                           ('text-align', 'center'), 
                                                           ('font-size', '10pt'), 
                                                           ('height', '40px')])])

styled_VUKE = data_VUKE.style.apply(lambda x: ['background: lightgreen' if x.name == 4 else '' for i in x], axis=1)\
         .set_properties(**{'width': '100px', 'text-align': 'center', 'font-size': '10pt'})\
         .set_table_styles([dict(selector='th', props=[('max-width', '80px'), 
                                                       ('text-align', 'center'), 
                                                       ('font-size', '10pt'), 
                                                       ('height', '40px')])])

styled_INRG = data_INRG.style.apply(lambda x: ['background: lightgreen' if x.name == 6 else '' for i in x], axis=1)\
         .set_properties(**{'width': '100px', 'text-align': 'center', 'font-size': '10pt'})\
         .set_table_styles([dict(selector='th', props=[('max-width', '80px'), 
                                                       ('text-align', 'center'), 
                                                       ('font-size', '10pt'), 
                                                       ('height', '40px')])])

styled_VUKG = data_VUKG.style.apply(lambda x: ['background: lightgreen' if x.name == 4 else '' for i in x], axis=1)\
         .set_properties(**{'width': '100px', 'text-align': 'center', 'font-size': '10pt'})\
         .set_table_styles([dict(selector='th', props=[('max-width', '80px'), 
                                                       ('text-align', 'center'), 
                                                       ('font-size', '10pt'), 
                                                       ('height', '40px')])])





selected_stock = st.selectbox('Select Security:', ['VUSA (S&P 500)', 'VUKE (FTSE 100)', 'INRG (iShares Global Clean Energy)', 'VUKG (FTSE 100 Growth)'])

if selected_stock == 'VUSA (S&P 500)':
    st.markdown(styled_VUSA.to_html(), unsafe_allow_html=True)
    st.markdown("")
    st.markdown("<small>The algorithm performs well with VUSA when investing following positive predictions, beating out the market rate.</small>", unsafe_allow_html=True)
    st.markdown("<small>The best investment strategy appears to be holding for 7 days: It has the highest daily return and capital growth.</small>", unsafe_allow_html=True)

elif selected_stock == 'VUKE (FTSE 100)':
    st.markdown(styled_VUKE.to_html(), unsafe_allow_html=True)
    st.markdown("")
    st.markdown("<small>The algorithm performs well with VUKE when investing following positive predictions, beating out the market rate.</small>", unsafe_allow_html=True)
    st.markdown("<small>The best investment strategy appears to be holding for 5 days: It has the highest daily return and capital growth. .</small>", unsafe_allow_html=True)
    st.markdown("Holding for 2 days might be seen as an alternative, safer option. It has a slightly lower return, but the MAE suggests predicitons are more accurate.")

elif selected_stock == 'INRG (iShares Global Clean Energy)':
    st.markdown(styled_INRG.to_html(), unsafe_allow_html=True)
    st.markdown("")
    st.markdown("<small>The algorithm performs well with INRG when investing following positive predictions, beating out the market rate.</small>", unsafe_allow_html=True)
    st.markdown("<small>The best investment strategy appears to be holding for 7 days.</small>", unsafe_allow_html=True)
    st.markdown("<small>Holding for 9 days has a slightly higher return, the MAE is significantly higher, so it makes sense to go for the marginally less profitable option, with less risk. Of course, this depends on personal risk preferences.</small>", unsafe_allow_html=True)

elif selected_stock == 'VUKG (FTSE 100 Growth)':
    st.markdown(styled_VUKG.to_html(), unsafe_allow_html=True)
    st.markdown("")
    st.markdown("<small>The algorithm performs well with VUKG when investing following positive predictions, beating out the market rate.</small>", unsafe_allow_html=True)
    st.markdown("<small>The best investment strategy appears to be holding for 5 days. It has the highest daily return and capital growth.</small>", unsafe_allow_html=True)
    st.markdown("<small>Holding for 9 days has a slightly higher return, the MAE is significantly higher, so it makes sense to go for the marginally less profitable option, with less risk. Of course, this depends on personal risk preferences.</small>", unsafe_allow_html=True)

st.markdown("")
st.markdown("")


optimal_strategies.append(get_optimal_strategy(data_VUSA, 'VUSA (S&P 500)'))
optimal_strategies.append(get_optimal_strategy(data_VUKE, 'VUKE (FTSE 100)'))
optimal_strategies.append(get_optimal_strategy(data_INRG, 'INRG (iShares Global Clean Energy)'))
optimal_strategies.append(get_optimal_strategy(data_VUKG, 'VUKG (FTSE 100 Growth)'))


st.subheader('Choosing The Best Investment')

st.markdown("<small>On any given day, the algorithm might suggest several investments. We need to decide which are the most profitable to target.</small>", unsafe_allow_html=True)
st.markdown("<small>We will compare out previously identified optimal strategies for each security, and compile a ranking.</small>", unsafe_allow_html=True)

if optimal_strategies:
    result_df = pd.concat(optimal_strategies)
    
    # Reorder the columns
    result_df = result_df[['Security', 'Daily Return with Positive Prediction Strategy', 'Capital with Positive Prediction Strategy', 'Average MAE', 'Days Holding']]
    
    # Convert 'Daily Return with Positive Prediction Strategy' to float for sorting
    result_df.loc[:, 'Daily Return with Positive Prediction Strategy'] = result_df['Daily Return with Positive Prediction Strategy'].str.replace('%','').astype(float)
    
    # Sort the dataframe based on 'Daily Return with Positive Prediction Strategy' and reset the index
    result_df = result_df.sort_values(by='Daily Return with Positive Prediction Strategy', ascending=False).reset_index(drop=True)
    
    # Create the 'Priority' column
    result_df['Priority'] = result_df.index + 1
    
    # Move 'Priority' column to the first position
    cols = result_df.columns.tolist()
    cols = [cols[-1]] + cols[:-1]
    result_df = result_df[cols]

    
    # Create a styling function
    def style_optimal_table(data):
        # Apply your styling here; no background highlighting in this version
        styled = data.style.set_properties(**{'width': '100px', 'text-align': 'center', 'font-size': '10pt'})\
                          .set_table_styles([dict(selector='th', props=[('max-width', '80px'), 
                                                                        ('text-align', 'center'), 
                                                                        ('font-size', '10pt'), 
                                                                        ('height', '40px')])])
        return styled

    # Apply the styling function to your result_df
    styled_result_df = style_optimal_table(result_df)
    
    # Display the styled dataframe in HTML
    st.markdown(styled_result_df.to_html(), unsafe_allow_html=True)





 
