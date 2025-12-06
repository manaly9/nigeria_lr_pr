import pandas as pd
import streamlit as st


@st.cache_data
def load_data():
    # Full dataset for 36 States + FCT
    data = [
        {"State": "Abia", "Region": "South East", "Population": 3727347, "GDP_Billions_Naira": 1900, "Literacy_Rate": 94.0, "Poverty_Rate": 30.0},
        {"State": "Adamawa", "Region": "North East", "Population": 4248436, "GDP_Billions_Naira": 1100, "Literacy_Rate": 55.0, "Poverty_Rate": 75.0},
        {"State": "Akwa Ibom", "Region": "South South", "Population": 5482177, "GDP_Billions_Naira": 3900, "Literacy_Rate": 93.0, "Poverty_Rate": 26.0},
        {"State": "Anambra", "Region": "South East", "Population": 5527809, "GDP_Billions_Naira": 2300, "Literacy_Rate": 92.0, "Poverty_Rate": 18.0},
        {"State": "Bauchi", "Region": "North East", "Population": 6537314, "GDP_Billions_Naira": 1000, "Literacy_Rate": 40.0, "Poverty_Rate": 61.0},
        {"State": "Bayelsa", "Region": "South South", "Population": 2277961, "GDP_Billions_Naira": 2800, "Literacy_Rate": 88.0, "Poverty_Rate": 22.0},
        {"State": "Benue", "Region": "North Central", "Population": 5741815, "GDP_Billions_Naira": 1400, "Literacy_Rate": 65.0, "Poverty_Rate": 33.0},
        {"State": "Borno", "Region": "North East", "Population": 5860183, "GDP_Billions_Naira": 900, "Literacy_Rate": 35.0, "Poverty_Rate": 60.0},
        {"State": "Cross River", "Region": "South South", "Population": 3866269, "GDP_Billions_Naira": 1800, "Literacy_Rate": 89.0, "Poverty_Rate": 36.0},
        {"State": "Delta", "Region": "South South", "Population": 5663362, "GDP_Billions_Naira": 4200, "Literacy_Rate": 85.0, "Poverty_Rate": 25.0},
        {"State": "Ebonyi", "Region": "South East", "Population": 2880383, "GDP_Billions_Naira": 900, "Literacy_Rate": 78.0, "Poverty_Rate": 45.0},
        {"State": "Edo", "Region": "South South", "Population": 4235595, "GDP_Billions_Naira": 2400, "Literacy_Rate": 87.0, "Poverty_Rate": 19.0},
        {"State": "Ekiti", "Region": "South West", "Population": 3270798, "GDP_Billions_Naira": 1200, "Literacy_Rate": 95.0, "Poverty_Rate": 28.0},
        {"State": "Enugu", "Region": "South East", "Population": 4411119, "GDP_Billions_Naira": 1400, "Literacy_Rate": 90.0, "Poverty_Rate": 28.0},
        {"State": "FCT (Abuja)", "Region": "North Central", "Population": 3564126, "GDP_Billions_Naira": 3800, "Literacy_Rate": 88.0, "Poverty_Rate": 20.0},
        {"State": "Gombe", "Region": "North East", "Population": 3256962, "GDP_Billions_Naira": 850, "Literacy_Rate": 45.0, "Poverty_Rate": 62.0},
        {"State": "Imo", "Region": "South East", "Population": 5408756, "GDP_Billions_Naira": 1900, "Literacy_Rate": 96.0, "Poverty_Rate": 21.0},
        {"State": "Jigawa", "Region": "North West", "Population": 5828163, "GDP_Billions_Naira": 1100, "Literacy_Rate": 43.0, "Poverty_Rate": 72.0},
        {"State": "Kaduna", "Region": "North West", "Population": 8252366, "GDP_Billions_Naira": 2100, "Literacy_Rate": 53.0, "Poverty_Rate": 43.5},
        {"State": "Kano", "Region": "North West", "Population": 13041001, "GDP_Billions_Naira": 2500, "Literacy_Rate": 48.0, "Poverty_Rate": 55.1},
        {"State": "Katsina", "Region": "North West", "Population": 7831319, "GDP_Billions_Naira": 1300, "Literacy_Rate": 45.0, "Poverty_Rate": 56.0},
        {"State": "Kebbi", "Region": "North West", "Population": 4440050, "GDP_Billions_Naira": 950, "Literacy_Rate": 40.0, "Poverty_Rate": 70.0},
        {"State": "Kogi", "Region": "North Central", "Population": 4473490, "GDP_Billions_Naira": 1300, "Literacy_Rate": 70.0, "Poverty_Rate": 30.0},
        {"State": "Kwara", "Region": "North Central", "Population": 3192928, "GDP_Billions_Naira": 1100, "Literacy_Rate": 70.0, "Poverty_Rate": 30.0},
        {"State": "Lagos", "Region": "South West", "Population": 15388000, "GDP_Billions_Naira": 8000, "Literacy_Rate": 96.5, "Poverty_Rate": 4.5},
        {"State": "Nasarawa", "Region": "North Central", "Population": 2523395, "GDP_Billions_Naira": 900, "Literacy_Rate": 60.0, "Poverty_Rate": 35.0},
        {"State": "Niger", "Region": "North Central", "Population": 5556247, "GDP_Billions_Naira": 1250, "Literacy_Rate": 58.0, "Poverty_Rate": 38.0},
        {"State": "Ogun", "Region": "South West", "Population": 5217716, "GDP_Billions_Naira": 3200, "Literacy_Rate": 90.0, "Poverty_Rate": 15.0},
        {"State": "Ondo", "Region": "South West", "Population": 4671695, "GDP_Billions_Naira": 1800, "Literacy_Rate": 84.0, "Poverty_Rate": 20.0},
        {"State": "Osun", "Region": "South West", "Population": 4705589, "GDP_Billions_Naira": 1600, "Literacy_Rate": 80.0, "Poverty_Rate": 25.0},
        {"State": "Oyo", "Region": "South West", "Population": 7840864, "GDP_Billions_Naira": 2800, "Literacy_Rate": 89.0, "Poverty_Rate": 22.0},
        {"State": "Plateau", "Region": "North Central", "Population": 4200442, "GDP_Billions_Naira": 1200, "Literacy_Rate": 75.0, "Poverty_Rate": 40.0},
        {"State": "Rivers", "Region": "South South", "Population": 7303924, "GDP_Billions_Naira": 5000, "Literacy_Rate": 92.1, "Poverty_Rate": 23.0},
        {"State": "Sokoto", "Region": "North West", "Population": 4998090, "GDP_Billions_Naira": 1050, "Literacy_Rate": 35.0, "Poverty_Rate": 80.0},
        {"State": "Taraba", "Region": "North East", "Population": 3066834, "GDP_Billions_Naira": 850, "Literacy_Rate": 45.0, "Poverty_Rate": 65.0},
        {"State": "Yobe", "Region": "North East", "Population": 3294137, "GDP_Billions_Naira": 700, "Literacy_Rate": 30.0, "Poverty_Rate": 72.0},
        {"State": "Zamfara", "Region": "North West", "Population": 4515427, "GDP_Billions_Naira": 800, "Literacy_Rate": 32.0, "Poverty_Rate": 74.0},
    ]
    
    df = pd.DataFrame(data)
    return df