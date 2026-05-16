import sqlite3
import pandas as pd
import streamlit as st
import json

st.set_page_config(
    page_title="Supply Chain ERP Module", 
    page_icon="📦", 
    layout="wide"
)

# 1. Connect to the database and cache the resource to prevent reloading on every interaction
@st.cache_resource
def init_db():
    # Use check_same_thread=False for Streamlit compatibility
    conn = sqlite3.connect('erp_data.db', check_same_thread=False)
    cursor = conn.cursor()
    
    # 2. Create the Purchase Orders table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Purchase_Orders (
        PO_Number TEXT PRIMARY KEY,
        Vendor_Name TEXT,
        Item_Ordered TEXT,
        Qty_Ordered INTEGER,
        Total_Cost REAL,
        Status TEXT
    )
    ''')
    
    # 3. Insert real-world healthcare test data 
    cursor.execute("INSERT OR IGNORE INTO Purchase_Orders VALUES ('PO-2001', 'Moffitt Cancer Center', 'Surgical Masks', 500, 250.00, 'Open')")
    cursor.execute("INSERT OR IGNORE INTO Purchase_Orders VALUES ('PO-2002', 'City of Hope', 'Exam Gloves', 1000, 150.00, 'Closed')")
    conn.commit()
    
    return conn

conn = init_db()

# 4. Build the Web Interface
st.title("📦 Supply Chain ERP Module")
st.markdown("Welcome to the Procure-to-Pay tracking system.")

# 5. Fetch the data
df = pd.read_sql_query("SELECT * FROM Purchase_Orders", conn)

# Display Top-Level Metrics for a dashboard feel
st.write("### Overview")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total Purchase Orders", value=len(df))
with col2:
    total_spend = df['Total_Cost'].sum()
    st.metric(label="Total Spend", value=f"${total_spend:,.2f}")
with col3:
    open_orders = len(df[df['Status'] == 'Open'])
    st.metric(label="Open Orders", value=open_orders)

st.divider()
st.subheader("Recent Purchase Orders")

# Apply styling to the status column
def color_status(val):
    color = '#22c55e' if val == 'Closed' else '#eab308' # Tailwind Green and Yellow
    return f'color: {color}; font-weight: bold'

# Use .map() for styling (modern pandas approach)
styled_df = df.style.map(color_status, subset=['Status'])

# Display dataframe using full container width
st.dataframe(styled_df, use_container_width=True, hide_index=True)

st.divider()
st.subheader("🤖 AI Supply Chain Insights")

with st.expander("Generate AI Insights from your Data"):
    st.write("Connect to Gemini to analyze your procurement data and get actionable summaries.")
    
    # Securely accept API key via Streamlit text input
    api_key = st.text_input("Enter your Gemini API Key:", type="password")
    
    if st.button("Analyze Data"):
        if not api_key:
            st.warning("Please enter an API key to proceed.")
        else:
            with st.spinner("Analyzing procurement data..."):
                try:
                    # Import dynamically so the app doesn't crash if the user hasn't installed the library yet
                    import google.generativeai as genai
                    
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    
                    # System prompt instructing the AI how to behave
                    prompt = f"""
                    Act as an expert Supply Chain & Financial Analyst. 
                    Provide a concise summary of this purchase order data. 
                    Highlight total spend, open orders, and operational insights.
                    Limit your response to 3-4 sentences. Use basic markdown.
                    
                    Data to Analyze: 
                    {df.to_dict(orient='records')}
                    """
                    
                    response = model.generate_content(prompt)
                    st.info(response.text)
                    
                except ImportError:
                    st.error("Missing dependency! Please run `pip install google-generativeai` in your terminal to use this feature.")
                except Exception as e:
                    st.error(f"Failed to generate insights: {str(e)}")
