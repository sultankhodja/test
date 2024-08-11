import streamlit as st
import sqlite3
from datetime import datetime
import pytz

# Set the page title and layout
st.set_page_config(page_title="EV Charger Reporting System", layout="centered")

# Define admin credentials
ADMIN_CREDENTIALS = {
    "admin": "admin_password"
}

# Function to connect to the database (new database file)
def get_connection():
    conn = sqlite3.connect('new_reports.db')  # Change the database file name here
    return conn

# Function to create a table if it doesn't exist
def create_table():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reports
                 (id INTEGER PRIMARY KEY, timestamp TEXT, charger_id TEXT, status TEXT, image BLOB)''')
    conn.commit()
    conn.close()

# Function to save data in the database
def save_data(charger_id, status, image):
    try:
        utc_time = datetime.now(pytz.utc)
        timestamp = utc_time.strftime("%Y-%m-%d %H:%M:%S")
        conn = get_connection()
        c = conn.cursor()
        c.execute("INSERT INTO reports (timestamp, charger_id, status, image) VALUES (?, ?, ?, ?)", 
                  (timestamp, charger_id, status, image))
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"An error occurred while saving data: {e}")
    finally:
        conn.close()

# Function to get all reports from the database
def get_reports(limit=None):
    conn = get_connection()
    c = conn.cursor()
    query = "SELECT timestamp, charger_id, status, image FROM reports ORDER BY timestamp DESC"
    if limit:
        query += f" LIMIT {limit}"
    
    try:
        c.execute(query)
        rows = c.fetchall()
        if not rows:
            st.info("No reports found in the database.")
        return rows
    except sqlite3.Error as e:
        st.error(f"An error occurred: {e}")
        return []
    finally:
        conn.close()

# User authentication
def authenticate(username, password):
    return ADMIN_CREDENTIALS.get(username) == password

# Main function
def main():
    # Create the reports table in the new database
    create_table()

    st.markdown("### Recent Reports")
    st.info("Here are the most recent issues reported by users.")

    # Display the most recent reports with Streamlit widgets
    reports = get_reports(limit=5)  # Limiting to 5 recent reports for display
    if reports:
        for report in reports:
            with st.expander(f"Issue reported on {report[0]}", expanded=False):
                st.markdown(f"**Charger ID:** {report[1]}")
                st.markdown(f"**Status:** {report[2]}")
                if report[3]:
                    st.image(report[3], caption="Uploaded Image", use_column_width=True)
    else:
        st.write("No recent reports available.")

    st.markdown("### Report an Issue with the Level 2 Charger at Roble Field Garage")

    # Placeholder for the report form
    report_form = st.empty()

    # Display form for reporting
    with report_form.form(key='report_form'):
        st.markdown("#### Please provide the status of the EV charger:")

        # Charger ID input
        charger_id = st.text_input("Charger ID (if known):")

        # Charging Issues
        st.markdown("##### ⚡ Charging Issues")
        col1, col2 = st.columns(2)
        with col1:
            slow = st.checkbox("🐢 Charging too slow", key="slow")
        with col2:
            not_charging = st.checkbox("❌ Not charging", key="not_charging")

        # Physical Damage
        st.markdown("##### 🛠️ Physical Damage")
        col3, col4 = st.columns(2)
        with col3:
            cable = st.checkbox("🔌 Damaged cable or connector", key="cable")
        with col4:
            unit = st.checkbox("🔧 Damaged charger unit", key="unit")

        # Connection Problems
        st.markdown("##### 📡 Connection Problems")
        col5, col6, col7, col8 = st.columns(4)
        with col5:
            app = st.checkbox("📱 App not working", key="app")
        with col6:
            start_stop = st.checkbox("🚫 Cannot start/stop charging", key="start_stop")
        with col7:
            payment = st.checkbox("💳 Payment issues", key="payment")
        with col8:
            network = st.checkbox("🌐 Network issues", key="network")

        # General Issues
        st.markdown("##### ⚙️ General Issues")
        col9, col10, col11, col12 = st.columns(4)
        with col9:
            power = st.checkbox("🔋 Power supply issues", key="power")
        with col10:
            overheating = st.checkbox("🔥 Overheating", key="overheating")
        with col11:
            installation = st.checkbox("🏗️ Installation problems", key="installation")
        with col12:
            other = st.checkbox("❓ Other (Please specify)", key="other")

        other_issue_description = st.text_input("If 'Other', please specify:")
        uploaded_file = st.file_uploader("Upload a picture (optional)", type=["jpg", "jpeg", "png"])

        submit_button = st.form_submit_button(label="Submit")

    # Submission response
    if submit_button:
        selected_issues = []
        issue_labels = [
            ("Charging too slow", slow), ("Not charging", not_charging),
            ("Damaged cable or connector", cable), ("Damaged charger unit", unit),
            ("App not working", app), ("Cannot start/stop charging", start_stop),
            ("Payment issues", payment), ("Network issues", network),
            ("Power supply issues", power), ("Overheating", overheating),
            ("Installation problems", installation), ("Other", other)
        ]

        for label, is_checked in issue_labels:
            if is_checked:
                selected_issues.append(label)
        
        if other_issue_description:
            selected_issues.append(f"Other: {other_issue_description}")

        status = ", ".join(selected_issues)
        
        if uploaded_file is not None:
            image = uploaded_file.read()
        else:
            image = None
        
        save_data(charger_id, status, image)
        report_form.empty()  # Clear the form
        st.balloons()
        st.success("Thank you for helping improve our community!")

    # Admin login section
    with st.expander("Admin Login"):
        login_form = st.empty()  # Placeholder for login form
        with login_form.form(key='admin_login_form'):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button(label="Login")

        if login_button:
            if authenticate(username, password):
                st.success(f"Logged in as {username}")
                login_form.empty()  # Remove login form after successful login
                st.markdown("## Reported Issues")
                reports = get_reports()
                if reports:
                    # Filter data
                    filter_text = st.text_input("Filter reports by status:")
                    filtered_reports = [report for report in reports if filter_text.lower() in report[2].lower()] if filter_text else reports

                    # Display reports
                    for report in filtered_reports:
                        st.write(f"Timestamp: {report[0]}")
                        st.write(f"Charger ID: {report[1]}")
                        st.write(f"Status: {report[2]}")
                        if report[3]:
                            st.image(report[3], caption="Uploaded Image", use_column_width=True)
                        st.markdown("---")
                else:
                    st.write("No reports available.")
            else:
                st.error("Invalid username or password")

# Run the app
if __name__ == "__main__":
    main()
