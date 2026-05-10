# imports
import streamlit as st
import pandas as pd
from model import calculate

st.title("Solar Project Calculator")

#recreating stateCosts

stateCosts = {"Alabama":16.79, "Alaska":26.57, "Arizona":15.62, "Arkansas":13.32, "California":33.75,
              "Colorado":16.33, "Connecticut":27.84, "Delaware":18.39, "Washington DC":24.03,
              "Florida":15.77, "Georgia": 14.60, "Hawaii":39.89, "Idaho":12.51, "Illinois":18.82,
              "Iowa":13.54, "Kansas":15.23, "Kentucky":13.68, "Louisiana": 12.44, "Maine":29.55, "Maryland":22.40,
              "Massachusetts":31.51, "Michigan":20.55, "Minnesota":16.44, "Mississippi":14.53, "Missouri":13.01,
              "Nebraska":13.19, "Nevada":13.83, "New Hampshire":27.39, "New Jersey":22.65, "New Mexico":15.00,
              "New York":27.07, "North Carolina":15.12, "North Dakota":12.87, "Ohio":17.93, "Oklahoma":14.48, 
              "Oregon":16.23, "Pennsylvania":20.58, "Rhode Island":31.30, "South Carolina":15.71, "South Dakota":14.15,
              "Tennessee":13.12, "Texas":16.18, "Utah":13.75, "Vermont":24.89, "Virginia":16.43, "Washington":14.12,
              "West Virginia":16.26, "Wisconsin":18.45, "Wyoming":15.18}

#User Inputs
state = st.selectbox("Select your state", list(stateCosts.keys())) # state input
roof_size = st.number_input("System size (kW DC)", min_value=1.0, value=1000.0) 
    # set an upper limit of 1000 kW based on a cursory google search. use min/max values for error handling

if st.button("Calculate"):
    # model call
    results = calculate(state, roof_size)

    # key metrics
    
    st.metric("Upfront Cost", f"${results['upfront_cost']:,.0f}")
    st.metric("Annual Generation", f"{results['annual_generation']:,.0f} kWh")
    st.metric("IRR", f"{results['irr']:.2%}")
    st.metric("Payback Period", f"{results['payback']} years")

    #col1, col2, col3, col4 = st.columns(4)
    #col1.metric("Upfront Cost", f"${results['upfront_cost']:,.0f}")
    #col2.metric("Annual Generation", f"{results['annual_generation']:,.0f} kWh")
    #col3.metric("IRR", f"{results['irr']:.2%}")
    #col4.metric("Payback Period", f"{results['payback']} years")
    
    # cash flow table
    st.subheader("25-Year Cash Flow")
    st.dataframe(results['table'], use_container_width=True)