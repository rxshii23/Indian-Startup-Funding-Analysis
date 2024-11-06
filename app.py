import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide', page_title='Indian Startup Funding Analysis')

df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'], errors='coerce')

df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

st.title('Indian Startup Funding')


def load_overall_analysis():
    st.title("Overall Analysis")

    #     total invested amount
    total = round(df['amount'].sum())

    #     maximum funding
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]

    #     avg funding
    avg_funding = round(df.groupby('startup')['amount'].sum().mean())

    #     total funded startups
    num_startups = df['startup'].nunique()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric('Total Investment', '₹ ' + str(total) + ' Cr')
    with col2:
        st.metric('Maximum Funding', '₹ ' + str(max_funding) + ' Cr')
    with col3:
        st.metric('Average Funding', '₹ ' + str(avg_funding) + ' Cr')
    with col4:
        st.metric('Funded Startups', str(num_startups))

    st.header('Month On Month Graph')
    selected_option = st.selectbox('Select Type', ['Total Amount Invested', 'No of Investments'])

    if selected_option == 'Total Amount Invested':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    figM, axM = plt.subplots()
    axM.plot(temp_df['x_axis'], temp_df['amount'])
    st.pyplot(figM)


def load_investor_details(investor):
    st.header(investor)
    #     load the recent 5 investments of the selected investor
    last5_df = df[df['investors'].str.contains(investor)].head()[
        ['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)

    #     biggest investments
    big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(
        ascending=False)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        # st.dataframe(big_series)

        #     graph
        st.subheader('Biggest Investments')
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)
        st.pyplot(fig)

    with col2:
        vertical_series2 = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Sector-wise Investments')
        fig2, ax2 = plt.subplots()
        ax2.pie(vertical_series2, labels=vertical_series2.index, autopct="%0.01f%%")
        st.pyplot(fig2)

    with col3:
        vertical_series3 = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader('Stage of Investments')
        fig3, ax3 = plt.subplots()
        ax3.pie(vertical_series3, labels=vertical_series3.index, autopct="%0.01f%%")
        st.pyplot(fig3)

    with col4:
        vertical_series4 = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum()
        st.subheader('Investments in Startups')
        fig4, ax4 = plt.subplots()
        ax4.pie(vertical_series4, labels=vertical_series4.index, autopct="%0.01f%%")
        st.pyplot(fig4)

    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader('Year on Year Investments')
    fig5, ax5 = plt.subplots()
    ax5.plot(year_series)
    st.pyplot(fig5)


st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'Startup', 'Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()

elif option == 'Startup':
    st.sidebar.selectbox('Select Startup', sorted(df['startup'].unique().tolist()))
    st.title('Startup Analysis')
    btn1 = st.sidebar.button('Find Startup Details')
elif option == 'Investor':
    selected_investor = st.sidebar.selectbox('Select Investor', sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        st.title('Investor Analysis')
        load_investor_details(selected_investor)
