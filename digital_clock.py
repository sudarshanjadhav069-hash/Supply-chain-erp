import streamlit as st
from datetime import datetime
import pytz

st.set_page_config(
    page_title="Digital Clock - Multi Timezone",
    page_icon="🕐",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .clock-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 20px;
        padding: 20px;
    }
    .timezone-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 25px;
        color: white;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        text-align: center;
        min-height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .timezone-name {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 10px;
        opacity: 0.9;
    }
    .time-display {
        font-size: 48px;
        font-weight: bold;
        font-family: 'Courier New', monospace;
        margin: 15px 0;
        letter-spacing: 2px;
    }
    .date-display {
        font-size: 14px;
        opacity: 0.85;
        margin-bottom: 8px;
    }
    .utc-offset {
        font-size: 12px;
        opacity: 0.8;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🕐 Digital Clock - Multi Timezone")
st.markdown("View current time across different timezones around the world")

# Sidebar controls
st.sidebar.header("⚙️ Settings")

# Preset timezones
preset_timezones = {
    "New York": "America/New_York",
    "London": "Europe/London",
    "Paris": "Europe/Paris",
    "Tokyo": "Asia/Tokyo",
    "Sydney": "Australia/Sydney",
    "Dubai": "Asia/Dubai",
    "Singapore": "Asia/Singapore",
    "Hong Kong": "Asia/Hong_Kong",
    "Mumbai": "Asia/Kolkata",
    "Bangkok": "Asia/Bangkok",
    "Los Angeles": "America/Los_Angeles",
    "Toronto": "America/Toronto",
}

# Allow users to select preset or custom timezones
use_preset = st.sidebar.checkbox("Use Preset Timezones", value=True)

if use_preset:
    selected_timezones = st.sidebar.multiselect(
        "Select Timezones:",
        list(preset_timezones.keys()),
        default=["New York", "London", "Tokyo", "Sydney"]
    )
    timezones = {name: preset_timezones[name] for name in selected_timezones}
else:
    # Get all available timezones
    all_timezones = pytz.all_timezones
    custom_selection = st.sidebar.multiselect(
        "Search and Select Timezones:",
        all_timezones,
        default=["America/New_York", "Europe/London", "Asia/Tokyo"]
    )
    timezones = {tz.split('/')[-1]: tz for tz in custom_selection}

# Auto-refresh option
auto_refresh = st.sidebar.checkbox("Auto Refresh (Every 1 Second)", value=True)
refresh_interval = st.sidebar.slider("Refresh Interval (seconds)", 1, 10, 1)

# Manual refresh button
if st.sidebar.button("🔄 Refresh Now"):
    st.rerun()

# Display current time in all selected timezones
st.divider()

if timezones:
    # Create a container for the clocks
    cols = st.columns(min(3, len(timezones)))
    
    for idx, (name, tz_str) in enumerate(timezones.items()):
        tz = pytz.timezone(tz_str)
        now = datetime.now(tz)
        
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%A, %B %d, %Y")
        utc_offset = now.strftime("%z")
        
        # Format UTC offset
        if utc_offset:
            utc_offset = f"UTC {utc_offset[:3]}:{utc_offset[3:]}"
        
        col = cols[idx % len(cols)]
        with col:
            st.markdown(f"""
                <div class="timezone-card">
                    <div class="timezone-name">{name}</div>
                    <div class="time-display">{time_str}</div>
                    <div class="date-display">{date_str}</div>
                    <div class="utc-offset">{utc_offset}</div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.warning("Please select at least one timezone to display")

# Auto-refresh using session state
if auto_refresh:
    st.markdown(f"""
        <meta http-equiv="refresh" content="{refresh_interval}">
    """, unsafe_allow_html=True)
    st.info(f"🔄 Auto-refreshing every {refresh_interval} second(s)")

st.divider()

# Footer with timezone info
st.markdown("""
### 📌 About
This digital clock displays the current time across multiple timezones simultaneously.
You can customize which timezones to display using the sidebar controls.

**Features:**
- ✅ Real-time updates every second
- ✅ 12+ preset timezones
- ✅ Access to all pytz timezones
- ✅ Shows date and UTC offset
- ✅ Beautiful responsive grid layout
""")
