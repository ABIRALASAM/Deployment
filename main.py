import streamlit as st
import pandas as pd
import numpy as np

URL = "https://raw.githubusercontent.com/marcopeix/MachineLearningModelDeploymentwithStreamlit/master/12_dashboard_capstone/data/quarterly_canada_population.csv"
@st.cache_data
def Read_data():
    df = pd.read_csv(URL, dtype={'Quarter': str,
                                 'Canada': np.int32,
                                 'Newfoundland and Labrador': np.int32,
                                 'Prince Edward Island': np.int32,
                                 'Nova Scotia': np.int32,
                                 'New Brunswick': np.int32,
                                 'Quebec': np.int32,
                                 'Ontario': np.int32,
                                 'Manitoba': np.int32,
                                 'Saskatchewan': np.int32,
                                 'Alberta': np.int32,
                                 'British Columbia': np.int32,
                                 'Yukon': np.int32,
                                 'Northwest Territories': np.int32,
                                 'Nunavut': np.int32})
    return df

if __name__ == '__main__':
    df = Read_data()
    st.header("Population of Canada")
    st.markdown(f"Source Table Can Be Found [here](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000901).")
    with st.expander("See full Data Table"):
        st.dataframe(df)

    with st.form(key='population-form'):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.header("Choose a Starting Date")
            qrt = st.selectbox(label="Quarter", options=[1, 2, 3, 4], key='start_qrt')
            strt = st.slider(label="Year", min_value=1991, max_value=2023, step=1, key='start_year')

        with col2:
            st.header("Choose an End Date")
            qrt2 = st.selectbox(label="Quarter", options=[1, 2, 3, 4], key='end_qrt')
            end = st.slider(label="Year", min_value=1991, max_value=2023, step=1, key='end_year')
        with col3:
            st.header("Choose a Location")
            lctn = st.selectbox(label="Location",
                                options= list(df.columns)[1:])
        sbmt = st.form_submit_button("Analyze")

        if sbmt:
            st.write(f"Starting date: Q{qrt} {strt}")
            st.write(f"Ending date: Q{qrt2} {end}")
            st.write(f"Location: {lctn}")
        if strt >= end:
            st.warning("your starting date is greater than the end date")
        else:
            tab1, tab2 = st.tabs(["Population", "Compare"])
            with tab1:
                st.header(f"Population change from Q{qrt} in {strt} to Q{qrt2} in {end} in {lctn}")
                if lctn in df.columns:
                    location_data = df[['Quarter', lctn]]

                    st.line_chart(location_data.set_index('Quarter'))
                else:
                    st.error(f"Location '{lctn}' not found in the data.")
            with tab2:
                mlt = st.multiselect(label="Select the Location",
                                     options=list(df.columns)[1:])
                if mlt:
                    # Filter the data to include only selected locations
                    selected_data = df[['Quarter'] + mlt]

                    # Ensure 'Quarter' is set as the index
                    selected_data.set_index('Quarter', inplace=True)
                    st.line_chart(selected_data)
