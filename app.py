import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configure page settings to match dark theme guidelines
st.set_page_config(page_title="Rheinmetall Geopolitical Risk Dashboard", layout="wide")

# Apply custom global CSS inject to lock the dark charcoal appearance (#1E2229)
st.markdown("""
    <style>
    .stApp { background-color: #1E2229; color: #FFFFFF; }
    div[data-testid="stMetricValue"] { color: #FFFFFF; font-size: 32px; font-weight: bold; }
    div[data-testid="stMetricLabel"] { color: #A6ACB8; font-size: 14px; }
    </style>
    """, unsafe_allowed_html=True)

# 1. LOAD DATA ARCHITECTURE FROM SECTION 1
@st.cache_data
def load_dashboard_data():
    asset_dim = pd.DataFrame([
        {"Facility_ID": "FAC_01", "Facility_Name": "Unterlüß Hub", "Country": "Germany", "Sovereign_Risk": 1},
        {"Facility_ID": "FAC_02", "Facility_Name": "Kassel Facility", "Country": "Germany", "Sovereign_Risk": 1},
        {"Facility_ID": "FAC_03", "Facility_Name": "Zalaegerszeg Plant", "Country": "Hungary", "Sovereign_Risk": 2},
        {"Facility_ID": "FAC_04", "Facility_Name": "Várpalota Complex", "Country": "Hungary", "Sovereign_Risk": 2},
        {"Facility_ID": "FAC_05", "Facility_Name": "Somerset West Hub", "Country": "South Africa", "Sovereign_Risk": 3},
        {"Facility_ID": "FAC_06", "Facility_Name": "Redbank MILVEHCOE", "Country": "Australia", "Sovereign_Risk": 1},
        {"Facility_ID": "FAC_07", "Facility_Name": "Ukraine Industry JV", "Country": "Ukraine", "Sovereign_Risk": 5}
    ])
    
    backlog_fact = pd.DataFrame([
        {"Facility_ID": "FAC_01", "Business_Division": "Weapon & Ammunition", "Backlog_Value_Billion_EUR": 32.5},
        {"Facility_ID": "FAC_02", "Business_Division": "Vehicle Systems", "Backlog_Value_Billion_EUR": 18.2},
        {"Facility_ID": "FAC_03", "Business_Division": "Vehicle Systems", "Backlog_Value_Billion_EUR": 11.5},
        {"Facility_ID": "FAC_04", "Business_Division": "Weapon & Ammunition", "Backlog_Value_Billion_EUR": 10.3},
        {"Facility_ID": "FAC_05", "Business_Division": "Weapon & Ammunition", "Backlog_Value_Billion_EUR": 3.5},
        {"Facility_ID": "FAC_06", "Business_Division": "Vehicle Systems", "Backlog_Value_Billion_EUR": 3.0},
        {"Facility_ID": "FAC_07", "Business_Division": "Vehicle Systems", "Backlog_Value_Billion_EUR": 1.0}
    ])
    
    backlog_history_fact = pd.DataFrame([
        {"Year": 2022, "Business_Division": "Weapon & Ammunition", "Backlog_Value_Billion_EUR": 11.2},
        {"Year": 2022, "Business_Division": "Vehicle Systems", "Backlog_Value_Billion_EUR": 15.4},
        {"Year": 2023, "Business_Division": "Weapon & Ammunition", "Backlog_Value_Billion_EUR": 16.5},
        {"Year": 2023, "Business_Division": "Vehicle Systems", "Backlog_Value_Billion_EUR": 21.8},
        {"Year": 2024, "Business_Division": "Weapon & Ammunition", "Backlog_Value_Billion_EUR": 20.1},
        {"Year": 2024, "Business_Division": "Vehicle Systems", "Backlog_Value_Billion_EUR": 28.5},
        {"Year": 2025, "Business_Division": "Weapon & Ammunition", "Backlog_Value_Billion_EUR": 25.8},
        {"Year": 2025, "Business_Division": "Vehicle Systems", "Backlog_Value_Billion_EUR": 36.2},
        {"Year": 2026, "Business_Division": "Weapon & Ammunition", "Backlog_Value_Billion_EUR": 32.5},
        {"Year": 2026, "Business_Division": "Vehicle Systems", "Backlog_Value_Billion_EUR": 47.5}
    ])

    supply_energy_fact = pd.DataFrame([
        {"Metric_ID": "SIG_201", "Facility_ID": "FAC_01", "Risk_Category": "Raw Material", "Signpost_Indicator": "Nitrocellulose Precursor Deficit (%)", "Green_Max": 5, "Red_Min": 16, "Current_Value": 18},
        {"Metric_ID": "SIG_202", "Facility_ID": "FAC_01", "Risk_Category": "Raw Material", "Signpost_Indicator": "Propellant Powder Lead Times (Mo)", "Green_Max": 2, "Red_Min": 6, "Current_Value": 6},
        {"Metric_ID": "SIG_203", "Facility_ID": "FAC_04", "Risk_Category": "Infrastructure", "Signpost_Indicator": "Parallel RDX Explosives Plant Delays (Days)", "Green_Max": 30, "Red_Min": 91, "Current_Value": 45},
        {"Metric_ID": "SIG_204", "Facility_ID": "FAC_04", "Risk_Category": "Infrastructure", "Signpost_Indicator": "Central European EEX Gas Spot Prices (€/MWh)", "Green_Max": 35, "Red_Min": 66, "Current_Value": 52},
        {"Metric_ID": "SIG_205", "Facility_ID": "FAC_05", "Risk_Category": "Infrastructure", "Signpost_Indicator": "Eskom Weekly Load-Shedding Outage Hours", "Green_Max": 4, "Red_Min": 13, "Current_Value": 18},
        {"Metric_ID": "SIG_206", "Facility_ID": "FAC_06", "Risk_Category": "Logistics", "Signpost_Indicator": "Drewry Maritime Steel Transit Delays (Days)", "Green_Max": 14, "Red_Min": 29, "Current_Value": 32}
    ])
    
    return asset_dim, backlog_fact, backlog_history_fact, supply_energy_fact

asset_dim, backlog_fact, backlog_history_fact, supply_energy_fact = load_dashboard_data()

# Process data elements using analytical model formulas
results = supply_energy_fact.apply(calculate_supply_risk_and_color, axis=1)
supply_energy_fact['Status'] = [r[0] for r in results]
supply_energy_fact['HEX_Color'] = [r[1] for r in results]
critical_alerts_count = (supply_energy_fact['Status'] == 'CRITICAL BOTTLENECK').sum()

# TOP ROW: HEADER ASSEMBLY
st.title("RHINEMETALL GEOPOLITICAL RISK ASSESSMENT: €80B BACKLOG BOTTLENECKS")
st.markdown("---")

# TOP ROW: Scoreboard & Slicer Parameter Layout
col_kpi1, col_kpi2, col_slicer = st.columns([1, 1, 2])

with col_kpi1:
    st.metric(label="TOTAL BACKLOG VOLUME", value="€80.0 Billion")
with col_kpi2:
    st.metric(label="ACTIVE CRITICAL ALERTS", value=f"{critical_alerts_count} Breached")
with col_slicer:
    shock_slider = st.slider("COMMODITY PRICE SHOCK SIMULATION SCENARIO (% INCREASE)", min_value=0.0, max_value=1.0, step=0.1, value=0.0)

# MIDDLE ROW: Grid View Configuration
col_grid_left, col_grid_right = st.columns([1, 1])

with col_grid_left:
    st.subheader("Asset Profiles: Capacity Tracking")
    profile_df = pd.merge(asset_dim, backlog_fact, on="Facility_ID")
    st.dataframe(profile_df[['Facility_Name', 'Country', 'Business_Division', 'Backlog_Value_Billion_EUR']], use_container_width=True, hide_index=True)

with col_grid_right:
    st.subheader("Ezzy's Supply Chain & Energy Signpost Matrix")
    # Apply threshold colors conditionally into matrix presentation layout
    styled_matrix = supply_energy_fact[['Risk_Category', 'Signpost_Indicator', 'Current_Value', 'Status']].style.background_gradient(cmap='Reds', subset=['Current_Value'])
    st.dataframe(styled_matrix, use_container_width=True, hide_index=True)

st.markdown("---")

# LOWER ROW: Dual-Axis Time Series Plot Tracking Inflections Since 2025
st.subheader("Annual Backlog Accumulation Layer (2022 - 2026 Trace)")
history_grouped = backlog_history_fact.groupby('Year')['Backlog_Value_Billion_EUR'].sum().reset_index()

fig_trend = go.Figure()
# Draw historical columns
for division in backlog_history_fact['Business_Division'].unique():
    div_data = backlog_history_fact[backlog_history_fact['Business_Division'] == division]
    fig_trend.add_trace(go.Bar(x=div_data['Year'], y=div_data['Backlog_Value_Billion_EUR'], name=division))
# Overlay cumulative trend line
fig_trend.add_trace(go.Scatter(x=history_grouped['Year'], y=history_grouped['Backlog_Value_Billion_EUR'], name="Total Accumulation Trajectory", line=dict(color='#FFD13B', width=3)))

fig_trend.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', barmode='stack', height=300)
st.plotly_chart(fig_trend, use_container_width=True)

# BOTTOM ROW: SCENARIO RISK GAUGE
st.subheader("Scenario Risk Capital Exposure Footer")
risk_capital = simulate_energy_price_shock(backlog_fact, supply_energy_fact, shock_slider)

fig_gauge = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = risk_capital,
    domain = {'x':, 'y': [0, 1]},
    title = {'text': "Total Backlog Capital Exposed Directly to Systemic Infrastructure Shocks (Billion EUR)", 'font': {'size': 14, 'color': '#A6ACB8'}},
    gauge = {
        'axis': {'range':, 'tickwidth': 1, 'tickcolor': "#FFFFFF"},
        'bar': {'color': "#FF4B4B"},
        'bgcolor': "#282D37",
        'steps': [
            {'range':, 'color': '#388E3C'},
            {'range':, 'color': '#FBC02D'},
            {'range':, 'color': '#D32F2F'}]}))

fig_gauge.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=220, margin=dict(t=30, b=10))
st.plotly_chart(fig_gauge, use_container_width=True)
