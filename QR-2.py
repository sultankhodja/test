#!/usr/bin/env python
# coding: utf-8

# In[9]:


# import streamlit as st
# import geocoder
# import requests
# import sqlite3
# from datetime import datetime

# # Set the page title and layout
# st.set_page_config(page_title="EV Charger Reporting System", layout="centered")

# # Define admin credentials
# ADMIN_CREDENTIALS = {
#     "admin": "admin_password"
# }

# # Function to connect to the database
# def get_connection():
#     conn = sqlite3.connect('reports.db')
#     return conn

# # Function to create a table if it doesn't exist
# def create_table():
#     conn = get_connection()
#     c = conn.cursor()
#     c.execute('''CREATE TABLE IF NOT EXISTS reports
#                  (id INTEGER PRIMARY KEY, timestamp TEXT, status TEXT, image BLOB, station_name TEXT, latitude REAL, longitude REAL)''')
#     conn.commit()
#     conn.close()

# # Function to alter the table and add missing columns
# def alter_table():
#     conn = get_connection()
#     c = conn.cursor()
#     # Add latitude column if it does not exist
#     try:
#         c.execute('ALTER TABLE reports ADD COLUMN latitude REAL')
#     except sqlite3.OperationalError:
#         pass  # Column already exists
#     # Add longitude column if it does not exist
#     try:
#         c.execute('ALTER TABLE reports ADD COLUMN longitude REAL')
#     except sqlite3.OperationalError:
#         pass  # Column already exists
#     conn.commit()
#     conn.close()

# # Function to save data in the database
# def save_data(status, image, station_name, latitude, longitude):
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     conn = get_connection()
#     c = conn.cursor()
#     c.execute("INSERT INTO reports (timestamp, status, image, station_name, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?)",
#               (timestamp, status, image, station_name, latitude, longitude))
#     conn.commit()
#     conn.close()

# # Function to get all reports from the database
# def get_reports():
#     conn = get_connection()
#     c = conn.cursor()
#     c.execute("SELECT timestamp, status, image, station_name, latitude, longitude FROM reports")
#     rows = c.fetchall()
#     conn.close()
#     return rows

# # User authentication
# def authenticate(username, password):
#     return ADMIN_CREDENTIALS.get(username) == password

# # Function to get the user's location based on their IP address
# def get_user_location():
#     g = geocoder.ip('me')
#     return g.latlng

# # Function to fetch EV charging stations from Open Charge Map
# def fetch_ev_charging_stations(api_key, latitude, longitude):
#     url = "https://api.openchargemap.io/v3/poi/"
#     params = {
#         'output': 'json',
#         'countrycode': 'US',
#         'latitude': latitude,
#         'longitude': longitude,
#         'maxresults': 50,    # Adjust the number of results as needed
#         'distance': 50,      # Distance in km
#         'key': api_key
#     }
#     response = requests.get(url, params=params)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         st.error(f"Error fetching data: {response.status_code}")
#         return []

# # Function to extract address information from API response
# def extract_station_addresses(stations_data):
#     addresses = []
#     for station in stations_data:
#         address_info = station['AddressInfo']
#         address_parts = [
#             address_info.get('AddressLine1', ''),
#             address_info.get('Town', ''),
#             address_info.get('StateOrProvince', ''),
#             address_info.get('Postcode', '')
#         ]
#         # Join non-empty address parts with a comma
#         address = ', '.join(part for part in address_parts if part)
#         addresses.append({
#             "name": address_info.get('Title', 'N/A'),
#             "address": address,
#             "latitude": address_info.get('Latitude', None),
#             "longitude": address_info.get('Longitude', None)
#         })
#     return addresses

# # Main function
# def main():
#     st.title("EV Charger Reporting System")

#     # Create the reports table and alter it if necessary
#     create_table()
#     alter_table()

#     # Detect the user's location
#     user_location = get_user_location()

#     # Display the user's location
#     if user_location:
#         latitude, longitude = user_location

#         # Fetch EV charging stations near the user's location
#         api_key = "8715bab8-2bf4-467b-81f7-dcfd469080c5"  # Your Open Charge Map API key
#         stations_data = fetch_ev_charging_stations(api_key, latitude, longitude)
#         addresses = extract_station_addresses(stations_data)

#         # Let the user select an EV charging station
#         if addresses:
#             station_options = [f"{station['name']} - {station['address']}" for station in addresses]
#             selected_station_index = st.selectbox("Select the EV charging station you are reporting:", range(len(station_options)), format_func=lambda x: station_options[x])
#             selected_station = addresses[selected_station_index]
#         else:
#             st.write("No nearby EV charging stations found.")
#             selected_station = {"name": "Unknown Location", "latitude": None, "longitude": None}
#     else:
#         st.write("Location not detected.")
#         selected_station = {"name": "Unknown Location", "latitude": None, "longitude": None}

#     st.success("We are a bunch of Stanford students working on a project to improve the conditions of EV chargers around the area. Your support is invaluable to us!")

#     # Placeholder for the report form
#     report_form = st.empty()

#     # Display form for reporting
#     with report_form.form(key='report_form'):
#         st.markdown("#### Please provide the status of the EV charger:")

#         # Charging Issues
#         st.markdown("##### ⚡ Charging Issues")
#         col1, col2 = st.columns(2)
#         with col1:
#             slow = st.checkbox("🐢 Charging too slow", key="slow")
#         with col2:
#             not_charging = st.checkbox("❌ Not charging", key="not_charging")

#         # Physical Damage
#         st.markdown("##### 🛠️ Physical Damage")
#         col3, col4 = st.columns(2)
#         with col3:
#             cable = st.checkbox("🔌 Damaged cable or connector", key="cable")
#         with col4:
#             unit = st.checkbox("🔧 Damaged charger unit", key="unit")

#         # Connection Problems
#         st.markdown("##### 📡 Connection Problems")
#         col5, col6, col7, col8 = st.columns(4)
#         with col5:
#             app = st.checkbox("📱 App not working", key="app")
#         with col6:
#             start_stop = st.checkbox("🚫 Cannot start/stop charging", key="start_stop")
#         with col7:
#             payment = st.checkbox("💳 Payment issues", key="payment")
#         with col8:
#             network = st.checkbox("🌐 Network issues", key="network")

#         # General Issues
#         st.markdown("##### ⚙️ General Issues")
#         col9, col10, col11, col12 = st.columns(4)
#         with col9:
#             power = st.checkbox("🔋 Power supply issues", key="power")
#         with col10:
#             overheating = st.checkbox("🔥 Overheating", key="overheating")
#         with col11:
#             installation = st.checkbox("🏗️ Installation problems", key="installation")
#         with col12:
#             other = st.checkbox("❓ Other (Please specify)", key="other")

#         other_issue_description = st.text_input("If 'Other', please specify:")
#         uploaded_file = st.file_uploader("Upload a picture (optional)", type=["jpg", "jpeg", "png"])

#         submit_button = st.form_submit_button(label="Submit")

#     # Submission response
#     if submit_button:
#         selected_issues = []
#         issue_labels = [
#             ("Charging too slow", slow), ("Not charging", not_charging),
#             ("Damaged cable or connector", cable), ("Damaged charger unit", unit),
#             ("App not working", app), ("Cannot start/stop charging", start_stop),
#             ("Payment issues", payment), ("Network issues", network),
#             ("Power supply issues", power), ("Overheating", overheating),
#             ("Installation problems", installation), ("Other", other)
#         ]

#         for label, is_checked in issue_labels:
#             if is_checked:
#                 selected_issues.append(label)
        
#         if other_issue_description:
#             selected_issues.append(f"Other: {other_issue_description}")

#         status = ", ".join(selected_issues)
        
#         if uploaded_file is not None:
#             image = uploaded_file.read()
#         else:
#             image = None
        
#         save_data(status, image, selected_station["name"], selected_station["latitude"], selected_station["longitude"])
#         report_form.empty()  # Clear the form
#         st.balloons()
#         st.success("Thank you for helping improve our community!")

#     # Admin login section
#     with st.expander("Admin Login"):
#         login_form = st.empty()  # Placeholder for login form
#         with login_form.form(key='admin_login_form'):
#             username = st.text_input("Username")
#             password = st.text_input("Password", type="password")
#             login_button = st.form_submit_button(label="Login")

#         if login_button:
#             if authenticate(username, password):
#                 st.success(f"Logged in as {username}")
#                 login_form.empty()  # Remove login form after successful login
#                 st.markdown("## Reported Issues")
#                 reports = get_reports()
#                 if reports:
#                     # Filter data
#                     filter_text = st.text_input("Filter reports by status:")
#                     filtered_reports = [report for report in reports if filter_text.lower() in report[1].lower()] if filter_text else reports

#                     # Display reports
#                     for report in filtered_reports:
#                         st.write(f"Timestamp: {report[0]}")
#                         st.write(f"Status: {report[1]}")
#                         st.write(f"Station: {report[3]}")
#                         st.write(f"Latitude: {report[4]}")
#                         st.write(f"Longitude: {report[5]}")
#                         if report[2]:
#                             st.image(report[2], caption="Uploaded Image", use_column_width=True)
#                         st.markdown("---")
#                 else:
#                     st.write("No reports available.")
#             else:
#                 st.error("Invalid username or password")

# # Run the app
# if __name__ == "__main__":
#     main()


# In[50]:


# import streamlit as st
# import sqlite3
# from datetime import datetime

# # Set the page title and layout
# st.set_page_config(page_title="EV Charger Reporting System", layout="centered")

# # Define admin credentials
# ADMIN_CREDENTIALS = {
#     "admin": "admin_password"
# }

# # Function to connect to the database
# def get_connection():
#     conn = sqlite3.connect('reports.db')
#     return conn

# # Function to create a table if it doesn't exist
# def create_table():
#     conn = get_connection()
#     c = conn.cursor()
#     c.execute('''CREATE TABLE IF NOT EXISTS reports
#                  (id INTEGER PRIMARY KEY, timestamp TEXT, status TEXT, image BLOB)''')
#     conn.commit()
#     conn.close()

# # Function to save data in the database
# def save_data(status, image):
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     conn = get_connection()
#     c = conn.cursor()
#     c.execute("INSERT INTO reports (timestamp, status, image) VALUES (?, ?, ?)", (timestamp, status, image))
#     conn.commit()
#     conn.close()

# # Function to get all reports from the database
# def get_reports(limit=None):
#     conn = get_connection()
#     c = conn.cursor()
#     query = "SELECT timestamp, status, image FROM reports ORDER BY timestamp DESC"
#     if limit:
#         query += f" LIMIT {limit}"
#     c.execute(query)
#     rows = c.fetchall()
#     conn.close()
#     return rows

# # User authentication
# def authenticate(username, password):
#     return ADMIN_CREDENTIALS.get(username) == password

# # Main function
# def main():
#     st.markdown("### Recent Reports")
#     st.info("Here are the most recent issues reported by users.")

#     # Display the most recent reports with Streamlit widgets
#     reports = get_reports(limit=5)  # Limiting to 5 recent reports for display
#     if reports:
#         for report in reports:
#             with st.expander(f"Issue reported on {report[0]}", expanded=False):
#                 st.markdown(f"**Status:** {report[1]}")
#                 if report[2]:
#                     st.image(report[2], caption="Uploaded Image", use_column_width=True)
#     else:
#         st.write("No recent reports available.")

#     st.markdown("### Report an Issue with the Level 2 Charger at Roble Field Garage")
#     st.success("We are a bunch of Stanford students working on a project to improve the conditions of EV chargers around the area. Your support is invaluable to us!")

#     # Create the reports table
#     create_table()

#     # Placeholder for the report form
#     report_form = st.empty()

#     # Display form for reporting
#     with report_form.form(key='report_form'):
#         st.markdown("#### Please provide the status of the EV charger:")

#         # Charging Issues
#         st.markdown("##### ⚡ Charging Issues")
#         col1, col2 = st.columns(2)
#         with col1:
#             slow = st.checkbox("🐢 Charging too slow", key="slow")
#         with col2:
#             not_charging = st.checkbox("❌ Not charging", key="not_charging")

#         # Physical Damage
#         st.markdown("##### 🛠️ Physical Damage")
#         col3, col4 = st.columns(2)
#         with col3:
#             cable = st.checkbox("🔌 Damaged cable or connector", key="cable")
#         with col4:
#             unit = st.checkbox("🔧 Damaged charger unit", key="unit")

#         # Connection Problems
#         st.markdown("##### 📡 Connection Problems")
#         col5, col6, col7, col8 = st.columns(4)
#         with col5:
#             app = st.checkbox("📱 App not working", key="app")
#         with col6:
#             start_stop = st.checkbox("🚫 Cannot start/stop charging", key="start_stop")
#         with col7:
#             payment = st.checkbox("💳 Payment issues", key="payment")
#         with col8:
#             network = st.checkbox("🌐 Network issues", key="network")

#         # General Issues
#         st.markdown("##### ⚙️ General Issues")
#         col9, col10, col11, col12 = st.columns(4)
#         with col9:
#             power = st.checkbox("🔋 Power supply issues", key="power")
#         with col10:
#             overheating = st.checkbox("🔥 Overheating", key="overheating")
#         with col11:
#             installation = st.checkbox("🏗️ Installation problems", key="installation")
#         with col12:
#             other = st.checkbox("❓ Other (Please specify)", key="other")

#         other_issue_description = st.text_input("If 'Other', please specify:")
#         uploaded_file = st.file_uploader("Upload a picture (optional)", type=["jpg", "jpeg", "png"])

#         submit_button = st.form_submit_button(label="Submit")

#     # Submission response
#     if submit_button:
#         selected_issues = []
#         issue_labels = [
#             ("Charging too slow", slow), ("Not charging", not_charging),
#             ("Damaged cable or connector", cable), ("Damaged charger unit", unit),
#             ("App not working", app), ("Cannot start/stop charging", start_stop),
#             ("Payment issues", payment), ("Network issues", network),
#             ("Power supply issues", power), ("Overheating", overheating),
#             ("Installation problems", installation), ("Other", other)
#         ]

#         for label, is_checked in issue_labels:
#             if is_checked:
#                 selected_issues.append(label)
        
#         if other_issue_description:
#             selected_issues.append(f"Other: {other_issue_description}")

#         status = ", ".join(selected_issues)
        
#         if uploaded_file is not None:
#             image = uploaded_file.read()
#         else:
#             image = None
        
#         save_data(status, image)
#         report_form.empty()  # Clear the form
#         st.balloons()
#         st.success("Thank you for helping improve our community!")

#     # Admin login section
#     with st.expander("Admin Login"):
#         login_form = st.empty()  # Placeholder for login form
#         with login_form.form(key='admin_login_form'):
#             username = st.text_input("Username")
#             password = st.text_input("Password", type="password")
#             login_button = st.form_submit_button(label="Login")

#         if login_button:
#             if authenticate(username, password):
#                 st.success(f"Logged in as {username}")
#                 login_form.empty()  # Remove login form after successful login
#                 st.markdown("## Reported Issues")
#                 reports = get_reports()
#                 if reports:
#                     # Filter data
#                     filter_text = st.text_input("Filter reports by status:")
#                     filtered_reports = [report for report in reports if filter_text.lower() in report[1].lower()] if filter_text else reports

#                     # Display reports
#                     for report in filtered_reports:
#                         st.write(f"Timestamp: {report[0]}")
#                         st.write(f"Status: {report[1]}")
#                         if report[2]:
#                             st.image(report[2], caption="Uploaded Image", use_column_width=True)
#                         st.markdown("---")
#                 else:
#                     st.write("No reports available.")
#             else:
#                 st.error("Invalid username or password")

# # Run the app
# if __name__ == "__main__":
#     main()

import streamlit as st
import sqlite3
from datetime import datetime

# Set the page title and layout
st.set_page_config(page_title="EV Charger Reporting System", layout="centered")

# Define admin credentials
ADMIN_CREDENTIALS = {
    "admin": "admin_password"
}

# Function to connect to the database
def get_connection():
    conn = sqlite3.connect('reports.db')
    return conn

# Function to create a table if it doesn't exist
def create_table():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reports
                 (id INTEGER PRIMARY KEY, timestamp TEXT, status TEXT, image BLOB)''')
    conn.commit()
    conn.close()

# Function to save data in the database
def save_data(status, image):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO reports (timestamp, status, image) VALUES (?, ?, ?)", (timestamp, status, image))
    conn.commit()
    conn.close()

# Function to get all reports from the database
def get_reports(limit=None):
    conn = get_connection()
    c = conn.cursor()
    query = "SELECT timestamp, status, image FROM reports ORDER BY timestamp DESC"
    if limit:
        query += f" LIMIT {limit}"
    
    try:
        c.execute(query)
        rows = c.fetchall()
    except sqlite3.Error as e:
        st.error(f"An error occurred: {e}")
        rows = []
    
    conn.close()
    return rows

# User authentication
def authenticate(username, password):
    return ADMIN_CREDENTIALS.get(username) == password

# Main function
def main():
    # Create the reports table
    create_table()

    st.markdown("### Recent Reports")
    st.info("Here are the most recent issues reported by users.")

    # Display the most recent reports with Streamlit widgets
    reports = get_reports(limit=5)  # Limiting to 5 recent reports for display
    if reports:
        for report in reports:
            with st.expander(f"Issue reported on {report[0]}", expanded=False):
                st.markdown(f"**Status:** {report[1]}")
                if report[2]:
                    st.image(report[2], caption="Uploaded Image", use_column_width=True)
    else:
        st.write("No recent reports available.")

    st.markdown("### Report an Issue with the Level 2 Charger at Roble Field Garage")
    st.success("We are a bunch of Stanford students working on a project to improve the conditions of EV chargers around the area. Your support is invaluable to us!")

    # Placeholder for the report form
    report_form = st.empty()

    # Display form for reporting
    with report_form.form(key='report_form'):
        st.markdown("#### Please provide the status of the EV charger:")

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
        
        save_data(status, image)
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
                    filtered_reports = [report for report in reports if filter_text.lower() in report[1].lower()] if filter_text else reports

                    # Display reports
                    for report in filtered_reports:
                        st.write(f"Timestamp: {report[0]}")
                        st.write(f"Status: {report[1]}")
                        if report[2]:
                            st.image(report[2], caption="Uploaded Image", use_column_width=True)
                        st.markdown("---")
                else:
                    st.write("No reports available.")
            else:
                st.error("Invalid username or password")

# Run the app
if __name__ == "__main__":
    main()
