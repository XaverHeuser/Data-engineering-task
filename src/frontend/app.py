import requests
import streamlit as st


API_URL = 'http://127.0.0.1:8000'


st.title('Streamlit Dashboard')

# Start ingestion
st.subheader('Start ingestion')
folder_path = st.text_input('Enter folder path: ', '')

if st.button('Start ingestion'):
    if folder_path.strip():
        with st.spinner('Contacting backend...'):
            response = requests.post(
                f'{API_URL}/start-ingestion?folder_path={folder_path}', timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                st.success(result)
            else:
                st.error('Error starting ingestion process')
    else:
        st.error('No folder path given')

# Price recommendations
st.subheader('Price recommendations')
if st.button('Get price recommendations'):
    response = requests.post(f'{API_URL}/price-recommendations', timeout=60)

    if response.status_code == 200:
        result = response.json()
        st.success(result)
    else:
        st.error('Failed to connect to the API.')

# Max recommendation
st.subheader('Max recommendation')
if st.button('Get max recommendation'):
    response = requests.get(f'{API_URL}/max-recommendation', timeout=60)

    if response.status_code == 200:
        result = response.json()
        st.json(result)
        st.write(
            f'product_id: {result.get("product_id")}, date: {result.get("date")}, Price Adjustment (%): {result.get("price_adjustment_pct")}'
        )

    else:
        st.error('Failed to connect to the API.')
