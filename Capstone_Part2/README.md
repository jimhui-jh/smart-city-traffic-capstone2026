```markdown
# pipeline.py purpose
This python script is to load the CSV file and validate the data before begins any data processing. It cleans the data by standardise inconsistent categorical values, missing values, identify duplicate rows and other cleaning data process.

# feature engineering.py purpose
This python script is to use the clean dataset to create time features, weather features, numerical features and traffic target.

# visualisation.py purpose
This python script is to present the Matplotlib of traffic demand by hour,weekday vs. weekend traffic and traffic and weather relationships, temperature vs traffic, traffic distribution and congestion patterns over time.There are three graphs in the traffic_analysis_plot which are traffic demand by hour of the Day,Comparison between weekday vs weekend traffic and average traffic volume by weather condition.

# User Guide: Metro Traffic Interactive Query Suite
This guide explains how to set up and run the standalone interactive traffic application on your own local computer or server.
## 1.To run this script, you need to have **Python 3** installed on your computer. 
We recommend using Python **3.8 or newer**.
pip install pandas numpy
## 2. Before launching, ensure you have both the script and the dataset file in the **same folder** on your machine:
Your-App-Folder/
mini_traffic_application.py                      # The Python script
Metro_Interstate_Traffic_Volume.csv # The traffic dataset (CSV)
## 3. How to Launch
1. Open your terminal or command prompt (cmd).
2. Navigate to your app directory using the `cd` command:
   ```bash
   cd path/to/Your-App-Folder
   ```
3. Execute the script using Python:
   ```bash
   mini_traffic_application.py
   ```
## 4. Navigating the App
users can select three different options on the metro traffic query.
=========================================================
🚗 METRO TRAFFIC INTERACTIVE QUERY SUITE 🚗
=========================================================
Options:
  1: Query traffic for a specific date/time
  2: Identify high-traffic periods
  3: Compare weekday and weekend traffic
  exit: Terminate the application
=========================================================
```
- **Type `1`** and press **Enter** to query for traffic patterns on specific dates and times. Users need to key-in correct format (e.g., typing `2016-08-10` returns hourly reports for that day).
- **Type `2`** and press **Enter** to know which periods where traffic exceeded a certain volume threshold (e.g., `5000` vehicles).
- **Type `3`** and press **Enter** to compare weekday vs. weekend averages traffic.
- **Type `exit`** to exit the application.
```