import streamlit as st
from datetime import datetime
import pytz

st.set_page_config(
    page_title="Digital Clock - Multi Timezone",
    page_icon="🕐",
    layout="wide"
)

st.title("🕐 Digital Clock - Multi Timezone")
st.markdown("Real-time clock displaying current time across different time zones.")

# Define time zones
timezones = {
    "UTC": "UTC",
    "New York": "America/New_York",
    "Los Angeles": "America/Los_Angeles",
    "London": "Europe/London",
    "Tokyo": "Asia/Tokyo",
    "Sydney": "Australia/Sydney",
    "Mumbai": "Asia/Kolkata",
    "Dubai": "Asia/Dubai",
    "Singapore": "Asia/Singapore",
    "Hong Kong": "Asia/Hong_Kong",
    "Berlin": "Europe/Berlin",
    "Paris": "Europe/Paris",
}

# Add custom timezone selector
col1, col2 = st.columns([3, 1])
with col1:
    st.write("### Select Additional Timezones")
with col2:
    if st.button("🔄 Refresh"):
        st.rerun()

# Allow user to add custom timezones
all_timezones = pytz.all_timezones
selected_timezones = st.multiselect(
    "Choose timezones to display:",
    options=all_timezones,
    default=list(timezones.values()),
    help="Select one or more timezones to display"
)

st.divider()

# Display clocks
if selected_timezones:
    # Get current UTC time
    utc_now = datetime.now(pytz.UTC)
    
    # Create columns for displaying clocks
    num_cols = 3
    cols = st.columns(num_cols)
    
    for idx, tz_name in enumerate(selected_timezones):
        col = cols[idx % num_cols]
        
        with col:
            try:
                # Get timezone object
                tz = pytz.timezone(tz_name)
                # Convert UTC time to target timezone
                local_time = utc_now.astimezone(tz)
                
                # Format the display
                time_str = local_time.strftime("%H:%M:%S")
                date_str = local_time.strftime("%A, %B %d, %Y")
                offset = local_time.strftime("%z")
                
                # Create a nice card display
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 20px;
                    border-radius: 10px;
                    text-align: center;
                    color: white;
                    margin: 10px 0;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                ">
                    <h3 style="margin: 0; font-size: 18px; margin-bottom: 10px;">{tz_name}</h3>
                    <div style="font-size: 36px; font-weight: bold; font-family: 'Courier New'; letter-spacing: 2px; margin: 15px 0;">
                        {time_str}
                    </div>
                    <div style="font-size: 14px; margin-bottom: 8px;">{date_str}</div>
                    <div style="font-size: 12px; opacity: 0.9;">UTC {offset[:3]}:{offset[3:]}</div>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error loading timezone {tz_name}: {str(e)}")
else:
    st.info("👆 Select at least one timezone to display the clock")

# Footer with auto-refresh info
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Current UTC Time", datetime.now(pytz.UTC).strftime("%H:%M:%S"))

with col2:
    selected_count = len(selected_timezones)
    st.metric("Timezones Selected", selected_count)

with col3:
    st.info("💡 Use 'Refresh' button to update times manually")

# Add auto-refresh using Streamlit's session state
st.markdown("""
<script>
    setTimeout(function() {
        window.location.reload();
    }, 1000);
</script>
""", unsafe_allow_html=True)
