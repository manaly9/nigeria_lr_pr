import base64

import pandas as pd
import plotly.express as px 
import streamlit as st

from nigeria_data import load_data

# --- PAGE CONFIG ---
st.set_page_config(page_title="Nigeria Economic Dashboard", layout="wide")

# --- GLASS UI & BACKGROUND SETUP ---
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = f"""
    <style>
    /* 1. GLOBAL SETTINGS */
    .block-container {{
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }}
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    [data-testid="stHeader"] {{ background-color: rgba(0,0,0,0); }}

    /* 2. GLASS CONTAINERS */
    div[data-testid="stVerticalBlockBorderWrapper"], div.stPlotlyChart {{
        background-color: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.5);
    }}

    /* 3. METRICS */
    [data-testid="stMetric"] {{
        background-color: white !important;
        padding: 5px !important;
    }}
    [data-testid="stMetricLabel"] p {{ color: #444 !important; font-weight: bold; font-size: 0.9rem !important; }}
    [data-testid="stMetricValue"] div {{ color: black !important; font-size: 1.8rem !important; }}

    /* 4. TEXT ELEMENTS */
    .title-box {{
        background-color: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(5px);
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 15px;
    }}
    .insight-box {{
        background-color: #e3f2fd;
        border-left: 5px solid #2196f3;
        padding: 15px;
        border-radius: 5px;
        color: #0d47a1;
        margin-bottom: 15px;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

try:
    set_background('background.jpg')
except FileNotFoundError:
    st.warning("⚠️ Image 'background.jpg' not found.")


# --- HEADER ---
st.markdown("""
<div class="title-box">
    <h1 style='color: #333; margin:0; text-align:center; font-size: 2.2rem;'>Nigeria Economic Intelligence</h1>
    <p style='color: #555; margin:0; font-weight: bold; text-align:center;'>Advanced Analytics: Geography, Economy & Demographics</p>
</div>
""", unsafe_allow_html=True)

df = load_data()

# --- SIDEBAR CONTROLS ---
st.sidebar.header("⚙️ Dashboard Controls")

view_mode = st.sidebar.radio(
    "Analysis Mode:",
    ["🔀 Filter Data", "📊 GDP Rank", "📚 Literacy Rank", "📉 Poverty Rank"]
)

filtered_df = df.copy() 
subtitle = "Overview"

# --- LOGIC ENGINE ---
if view_mode == "🔀 Filter Data":
    st.sidebar.divider()
    selected_regions = st.sidebar.multiselect("Region:", options=df["Region"].unique(), default=[])
    if not selected_regions:
        filtered_df = df
        subtitle = "National Overview"
    else:
        filtered_df = df[df["Region"].isin(selected_regions)]
        subtitle = f"Region: {', '.join(selected_regions)}"

elif view_mode == "📊 GDP Rank":
    sort_option = st.sidebar.radio("Sort By:", ["🏆 Top 5", "🔻 Bottom 5", "⬇️ All"])
    if sort_option == "🏆 Top 5": filtered_df = df.sort_values("GDP_Billions_Naira", ascending=False).head(5)
    elif sort_option == "🔻 Bottom 5": filtered_df = df.sort_values("GDP_Billions_Naira", ascending=True).head(5)
    else: filtered_df = df.sort_values("GDP_Billions_Naira", ascending=False)
    subtitle = "GDP Analysis"

elif view_mode == "📚 Literacy Rank":
    sort_option = st.sidebar.radio("Sort By:", ["🎓 Top 5", "⚠️ Bottom 5", "⬇️ All"])
    if sort_option == "🎓 Top 5": filtered_df = df.sort_values("Literacy_Rate", ascending=False).head(5)
    elif sort_option == "⚠️ Bottom 5": filtered_df = df.sort_values("Literacy_Rate", ascending=True).head(5)
    else: filtered_df = df.sort_values("Literacy_Rate", ascending=False)
    subtitle = "Literacy Analysis"

elif view_mode == "📉 Poverty Rank":
    sort_option = st.sidebar.radio("Sort By:", ["🛡️ Lowest (Best)", "🚨 Highest (Worst)"])
    if sort_option == "🛡️ Lowest (Best)": filtered_df = df.sort_values("Poverty_Rate", ascending=True).head(10)
    else: filtered_df = df.sort_values("Poverty_Rate", ascending=False).head(10)
    subtitle = "Poverty Analysis"

# --- NEW: DOWNLOAD BUTTON ---
st.sidebar.divider()
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    "📥 Download Report (CSV)",
    data=csv,
    file_name="nigeria_economic_data.csv",
    mime="text/csv",
    help="Download the currently filtered data for Excel."
)

filtered_df = filtered_df.reset_index(drop=True)
filtered_df.index = filtered_df.index + 1 

# --- METRICS ROW ---
with st.container(border=True):
    col1, col2, col3 = st.columns(3)
    col1.metric("States in View", len(filtered_df))
    col2.metric("Avg Literacy", f"{filtered_df['Literacy_Rate'].mean():.1f}%")
    col3.metric("Avg GDP", f"₦{filtered_df['GDP_Billions_Naira'].mean():,.0f}B")

# --- NEW: INTERACTIVE MAP (BUBBLE MAP) ---
# We put this at the top because it's the most visual element
with st.container(border=True):
    st.subheader("🌍 Geographic Economic Map")
    
    # Create the Map
    fig_map = px.scatter_mapbox(
        filtered_df,
        lat="Lat", lon="Lon",
        size="GDP_Billions_Naira", # Bubble size = GDP
        color="Region",            # Bubble color = Region
        hover_name="State",
        hover_data=["Population", "Literacy_Rate", "Poverty_Rate"],
        zoom=5,
        center={"lat": 9.0820, "lon": 8.6753}, # Center on Nigeria
        height=500,
        size_max=35,
        title="Bubble Map: Size represents GDP Strength"
    )
    fig_map.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":40,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)

# --- MAIN TABLE & FLOW ---
st.markdown(f"<h3 style='color: white; border-bottom: 2px solid #ddd; padding-bottom: 5px;'>{subtitle}</h3>", unsafe_allow_html=True)
left_col, right_col = st.columns([2, 1], gap="small")

with left_col:
    with st.container(border=True):
        st.dataframe(
            filtered_df.style.background_gradient(cmap="Greens", subset=["GDP_Billions_Naira"])
                             .background_gradient(cmap="Reds", subset=["Poverty_Rate"]),
            use_container_width=True, height=500
        )

with right_col:
    with st.container(border=True):
        st.markdown("<h4 style='text-align: center; color: #333;'>📊 Hierarchy Flow</h4>", unsafe_allow_html=True)
        if not filtered_df.empty:
            # Determine metric
            if view_mode == "📉 Poverty Rank" and "Lowest" in str(sort_option):
                top_s = filtered_df.iloc[0]; bot_s = filtered_df.iloc[-1]; m_col = "Poverty_Rate"; unit="%"; lbl="Poverty"
            elif view_mode == "📚 Literacy Rank":
                top_s = filtered_df.iloc[0]; bot_s = filtered_df.iloc[-1]; m_col = "Literacy_Rate"; unit="%"; lbl="Literacy"
            else:
                top_s = filtered_df.sort_values("GDP_Billions_Naira", ascending=False).iloc[0]
                bot_s = filtered_df.sort_values("GDP_Billions_Naira", ascending=False).iloc[-1]
                m_col = "GDP_Billions_Naira"; unit="B"; lbl="GDP"
            
            gap = top_s[m_col] - bot_s[m_col]

            # Cards
            st.markdown(f"""
            <div style="background-color:rgba(255,255,255,0.9); padding:10px; border-radius:10px; border-left:6px solid #28a745; margin-bottom:10px; text-align:center;">
                <strong style="color:#28a745;">🚀 Peak {lbl}</strong><br>
                <b>{top_s['State']}</b><br>{top_s[m_col]:,.0f}{unit}
            </div>
            <div style="background-color:rgba(255,255,255,0.9); padding:5px; border-radius:20px; border:1px dashed #ff4b4b; text-align:center; margin:10px 0;">
                <b style="color:#ff4b4b;">⬇️ Gap: {gap:,.0f}{unit} ⬇️</b>
            </div>
            <div style="background-color:rgba(255,255,255,0.9); padding:10px; border-radius:10px; border-left:6px solid #dc3545; margin-top:10px; text-align:center;">
                <strong style="color:#dc3545;">📉 Base {lbl}</strong><br>
                <b>{bot_s['State']}</b><br>{bot_s[m_col]:,.0f}{unit}
            </div>
            """, unsafe_allow_html=True)

            # --- NEW: AI INSIGHTS ---
            st.divider()
            st.markdown("#### 🤖 Auto-Insights")
            
            # Simple Logic-based "AI"
            insight = ""
            if filtered_df['Literacy_Rate'].mean() > 80:
                insight = "✅ <b>High Education Zone:</b> This selection represents a highly literate workforce."
            elif filtered_df['Poverty_Rate'].mean() > 50:
                insight = "⚠️ <b>Development Focus:</b> High poverty rates detected. Priority zone for economic intervention."
            else:
                insight = "ℹ️ <b>Balanced Mix:</b> This selection shows diverse economic conditions."
            
            st.markdown(f"<div class='insight-box'>{insight}</div>", unsafe_allow_html=True)

# --- NEW: CORRELATION CHART ---
with st.container(border=True):
    st.subheader("📈 Correlation Analysis: Money vs. Education")
    
    # Scatter Plot
    fig_corr = px.scatter(
        filtered_df,
        x="Literacy_Rate",
        y="Poverty_Rate",
        size="GDP_Billions_Naira",
        color="Region",
        hover_name="State",
        title="Does Literacy Reduce Poverty?",
        labels={"Literacy_Rate": "Literacy %", "Poverty_Rate": "Poverty %"},
        height=400
    )
    # Add trendline visually (just simple layout)
    st.plotly_chart(fig_corr, use_container_width=True)
    st.caption("Tip: Bigger bubbles = Higher GDP. Notice how as Literacy (X) goes up, Poverty (Y) usually goes down.")