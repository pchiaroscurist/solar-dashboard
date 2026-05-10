# imports
import numpy_financial as npf
import pandas as pd

def calculate(state, roofSize):

    # dictionary
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

    # given information
    installCost = roofSize * 2.5 * 1000; # 2.5$/W assumed, 1000:1 kW:W
    annualGeneration = 1400 * roofSize; # 1400 kWh/kW
    priceKicker = 1.025; # price escalates at 2.5% annually
    maintenaceCosts = 15; # $15/kW/year for maintenance (flat fee)

    # modeling
    yearZeroCF = -1 * installCost * 0.7; # 30% ITC @ year 0
    cashFlows = [yearZeroCF] # dict to store CF results
    electricityPrice = stateCosts[state]/100 # pulling electricity price from dict + converting cents to dollars

    for year in range(1, 26):
        revenue = annualGeneration * electricityPrice * (priceKicker ** year) # electricity produced * price modified by the price kicker of 2.5%
            # important to consider we aren't considering the TV of money + the interest rate 
        opmain = maintenaceCosts * roofSize
        cashFlows.append(revenue - opmain)

    # finding irr + payback

    irr = npf.irr(cashFlows)

    cumulative = 0
    payback = None
    for i, cf in enumerate(cashFlows):
        cumulative += cf
        if cumulative > 0 and payback is None:
            payback = i # when cumulative cash flows > 0, you found payback year

    table = pd.DataFrame({
    "Year": range(0, 26),
    "Cash Flow": cashFlows,
    "Cumulative Cash Flow": pd.Series(cashFlows).cumsum()
    })
    table["Cash Flow"] = table["Cash Flow"].map("${:,.2f}".format)
    table["Cumulative Cash Flow"] = table["Cumulative Cash Flow"].map("${:,.2f}".format)
    table = table.set_index("Year")
    
    return {
        "upfront_cost": installCost,
        "annual_generation": annualGeneration,
        "irr": irr,
        "payback": payback,
        "table": table
    }