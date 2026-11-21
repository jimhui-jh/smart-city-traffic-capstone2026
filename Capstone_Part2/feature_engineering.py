# %%
import pandas as pd

# Load the dataset
file_path = '/content/Metro_Interstate_Traffic_Volume.csv'
df = pd.read_csv(file_path)

# Display the shape and the first few rows of the dataset
print(f"Dataset shape: {df.shape}")
display(df.head())

# %%
import pandas as pd
import logging
import sys

# Configure logging to stdout so it works correctly in notebook cells
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True
)
logger = logging.getLogger('traffic_pipeline')

file_path = '/content/Metro_Interstate_Traffic_Volume.csv'

try:
    # Attempt to load the CSV dataset
    df = pd.read_csv(file_path)
    logger.info(f"Raw file successfully loaded. Loaded {df.shape[0]} rows and {df.shape[1]} columns.")
    display(df.head())
except FileNotFoundError:
    logger.error(f"The file at '{file_path}' was not found. Please verify the file path.")
    df = pd.DataFrame() # Fallback empty dataframe to prevent name errors downstream
except pd.errors.ParserError:
    logger.error("Failed to parse the CSV file. It might contain corrupted data or incorrect delimiters.")
    df = pd.DataFrame()
except pd.errors.EmptyDataError:
    logger.error("The CSV file is empty.")
    df = pd.DataFrame()
except Exception as e:
    logger.exception(f"An unexpected error occurred while reading the file: {e}")
    df = pd.DataFrame()

# %%
# Expected schema columns for the Metro Interstate Traffic Volume dataset
expected_columns = {
    'holiday', 'temp', 'rain_1h', 'snow_1h', 'clouds_all',
    'weather_main', 'weather_description', 'date_time', 'traffic_volume'
}

try:
    current_columns = set(df.columns)
    missing_columns = expected_columns - current_columns

    if missing_columns:
        error_msg = f"Schema validation failed. Missing expected columns: {list(missing_columns)}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    else:
        logger.info("Schema validation successful. All expected columns are present.")

except Exception as e:
    logger.error("The pipeline failed during schema validation.", exc_info=True)
    logger.error("Pipeline execution halted gracefully due to a validation error.")

# %%
import pandas as pd
import numpy as np
import sys

try:
    # 1. Check and handle missing values in 'holiday' column
    initial_rows = len(df)
    null_holiday_count = df['holiday'].isnull().sum()
    if null_holiday_count > 0:
        # We will impute the NaN values in holiday with 'None'
        df['holiday'] = df['holiday'].fillna('None')
        logger.warning(f"Imputed {null_holiday_count} missing values in the 'holiday' column with 'None'.")

    # 2. Check for temperature outliers (e.g., temp < 100 Kelvin is extremely abnormal for outdoor weather)
    temp_outliers = df[df['temp'] < 100]
    outlier_count = len(temp_outliers)
    if outlier_count > 0:
        # We will drop these rows
        df = df[df['temp'] >= 100]
        logger.warning(f"Dropped {outlier_count} rows due to extreme temperature outliers (< 100K).")

    # 3. Check for duplicates
    duplicates_count = df.duplicated().sum()
    if duplicates_count > 0:
        df = df.drop_duplicates()
        logger.warning(f"Dropped {duplicates_count} duplicate rows from the dataset.")
    else:
        logger.info("No duplicate rows identified during initial preprocessing.")

    logger.info(f"Data preprocessing complete. Final shape: {df.shape}")

except Exception as e:
    logger.error("The preprocessing pipeline failed to complete due to an error.", exc_info=True)
    logger.error("Pipeline execution halted gracefully due to an error. See logs for details.")

# %%
try:
    # Display unique values before standardization for reference
    logger.info(f"Unique weather categories before: {df['weather_main'].unique()}")

    # Standardize 'weather_main' and 'weather_description' to title case and strip whitespace
    for col in ['weather_main', 'weather_description', 'holiday']:
        if col in df.columns:
            original_series = df[col].astype(str)
            standardized_series = original_series.str.strip().str.title()

            # Track how many values changed
            changed_mask = original_series != standardized_series
            changed_count = changed_mask.sum()

            if changed_count > 0:
                df[col] = standardized_series
                logger.warning(f"Standardized inconsistent formatting in '{col}' column. Updated {changed_count} rows to title case.")

    logger.info(f"Categorical standardization complete. Unique weather categories now: {df['weather_main'].unique()}")

except Exception as e:
    logger.error("The pipeline failed during categorical standardization.", exc_info=True)
    logger.error("Pipeline execution halted gracefully due to a standardization error.")

# %%
try:
    # Display date_time type before conversion
    logger.info(f"'date_time' column data type before conversion: {df['date_time'].dtype}")

    # Convert 'date_time' to datetime objects. Invalid parsing will be coerced to NaT
    original_dates = df['date_time'].copy()
    df['date_time'] = pd.to_datetime(df['date_time'], errors='coerce')

    # Count if any invalid date strings turned into NaT
    null_dates_count = df['date_time'].isnull().sum()
    if null_dates_count > 0:
        logger.warning(f"Found and coerced {null_dates_count} invalid date/time values to NaT.")
        # Optional: drop rows with invalid date formats
        df = df.dropna(subset=['date_time'])
        logger.warning(f"Dropped {null_dates_count} rows containing invalid date/time values.")

    # Check and log the min and max date ranges
    min_date = df['date_time'].min()
    max_date = df['date_time'].max()
    logger.info(f"'date_time' column successfully parsed. Date range: {min_date} to {max_date}.")

except Exception as e:
    logger.error("The pipeline failed during date/time parsing and validation.", exc_info=True)
    logger.error("Pipeline execution halted gracefully due to a date/time validation error.")

# %%
try:
    # Count duplicates based on all columns
    duplicate_mask = df.duplicated()
    num_duplicates = duplicate_mask.sum()

    if num_duplicates > 0:
        logger.warning(f"Found {num_duplicates} duplicate rows in the current dataset.")
        # Remove the duplicates in-place or by reassignment
        df = df.drop_duplicates()
        logger.info(f"Successfully removed all {num_duplicates} duplicate rows. New dataset shape: {df.shape}")
    else:
        logger.info("No duplicate rows found. The dataset is already unique.")

except Exception as e:
    logger.error("The pipeline failed while identifying and removing duplicate rows.", exc_info=True)
    logger.error("Pipeline execution halted gracefully due to a deduplication error.")

# %%
try:
    # 1. Check for negative precipitation values
    negative_rain = df[df['rain_1h'] < 0]
    negative_snow = df[df['snow_1h'] < 0]

    if len(negative_rain) > 0:
        logger.warning(f"Detected {len(negative_rain)} records with negative rain_1h. Correcting values to 0.")
        df.loc[df['rain_1h'] < 0, 'rain_1h'] = 0.0

    if len(negative_snow) > 0:
        logger.warning(f"Detected {len(negative_snow)} records with negative snow_1h. Correcting values to 0.")
        df.loc[df['snow_1h'] < 0, 'snow_1h'] = 0.0

    # 2. Check for impossible cloud cover percentages (> 100% or < 0%)
    invalid_clouds = df[(df['clouds_all'] < 0) | (df['clouds_all'] > 100)]
    if len(invalid_clouds) > 0:
        logger.warning(f"Detected {len(invalid_clouds)} records with invalid cloud percentages. Clipping to [0, 100].")
        df['clouds_all'] = df['clouds_all'].clip(lower=0, upper=100)

    # 3. Check for extremely high precipitation outliers (e.g., rain_1h > 500mm/hr as unreasonable or a recorded anomaly)
    extreme_rain = df[df['rain_1h'] > 500]
    if len(extreme_rain) > 0:
        logger.warning(f"Detected {len(extreme_rain)} extreme rain anomalies (> 500mm/h). Correcting to median value.")
        median_rain = df.loc[df['rain_1h'] <= 500, 'rain_1h'].median()
        df.loc[df['rain_1h'] > 500, 'rain_1h'] = median_rain

    logger.info("Outlier detection and validation checks for precipitation and cloud metrics successfully completed.")

except Exception as e:
    logger.error("The pipeline failed during outlier detection and handling.", exc_info=True)
    logger.error("Pipeline execution halted gracefully due to an outlier validation error.")

# %%
try:
    # Ensure we have datetime helper columns for group-by-group operations
    if 'date_time' in df.columns:
        df['month'] = df['date_time'].dt.month
    else:
        df['month'] = 1  # Fallback if datetime is not parsed

    # 1. Identify sensor readings showing 0 Kelvin
    zero_kelvin_count = (df['temp'] == 0).sum()
    if zero_kelvin_count > 0:
        logger.warning(f"Detected {zero_kelvin_count} records with 0 Kelvin temperature. Removing these anomalies.")
        df = df[df['temp'] > 0]
        logger.info(f"Removed records with 0 Kelvin temperature. Current shape: {df.shape}")
    else:
        logger.info("No 0 Kelvin temperature anomalies detected.")

    # 2. Identify and handle physically implausible extreme rainfall values (> 500.0 mm in 1 hour)
    extreme_rainfall_threshold = 500.0
    extreme_rain_mask = df['rain_1h'] > extreme_rainfall_threshold
    extreme_rain_indices = df[extreme_rain_mask].index
    extreme_rain_count = len(extreme_rain_indices)

    if extreme_rain_count > 0:
        logger.warning(f"Detected {extreme_rain_count} records with physically implausible rainfall (> {extreme_rainfall_threshold} mm).")

        # Loop explicitly row-by-row over identified outliers to apply month-by-month imputation
        for idx in extreme_rain_indices:
            row_month = df.loc[idx, 'month']
            original_val = df.loc[idx, 'rain_1h']

            # Calculate median for this specific month excluding extreme outliers
            valid_month_rain = df[(df['month'] == row_month) & (df['rain_1h'] <= extreme_rainfall_threshold)]['rain_1h']

            if not valid_month_rain.empty:
                monthly_median = valid_month_rain.median()
            else:
                monthly_median = 0.0 # Fallback median

            df.loc[idx, 'rain_1h'] = monthly_median
            logger.info(f"Imputed outlier at index {idx} (Month: {row_month}, Original: {original_val} mm) with monthly median: {monthly_median} mm")
    else:
        logger.info("No physically implausible extreme rainfall values detected.")

    # Clean up temporary helper column
    df = df.drop(columns=['month'])

except Exception as e:
    logger.error("The custom group-by-group outlier detection pipeline failed.", exc_info=True)
    logger.error("Pipeline execution halted due to custom outlier detection error.")

# %%
# Validate and display statistics for 'temp' and 'rain_1h' to ensure outliers are imputed/removed using logging
try:
    logger.info("--- Validation Summary Post-Imputation ---")
    # Log descriptive statistics summary
    stats_summary = df[['temp', 'rain_1h']].describe().to_string()
    for line in stats_summary.split('\n'):
        logger.info(line)

    logger.info(f"Maximum rainfall value after imputation: {df['rain_1h'].max()} mm")
    logger.info(f"Minimum temperature value after cleaning: {df['temp'].min()} Kelvin")
except Exception as e:
    logger.error("Failed during post-imputation validation logging.", exc_info=True)

# %%
import numpy as np
import pandas as pd

try:
    logger.info("--- Engineering ML-Ready Features ---")

    # 1. Extract base time features
    df['hour'] = df['date_time'].dt.hour
    df['day_of_week'] = df['date_time'].dt.dayofweek
    df['month'] = df['date_time'].dt.month

    # 2. Extract binary weekend indicator (1 for Saturday/Sunday, 0 for Weekdays)
    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)

    # 3. Apply Cyclical Encodings (sine and cosine transforms) to preserve periodic time relationships
    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24.0)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24.0)
    df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12.0)
    df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12.0)

    # 4. Create Derived Weather Indicators
    # Freezing indicator: 1 if temperature is below 273.15 Kelvin (0°C), 0 otherwise
    df['is_freezing'] = (df['temp'] < 273.15).astype(int)

    # Rain occurrence indicator: 1 if rain_1h > 0, else 0
    df['is_raining'] = (df['rain_1h'] > 0).astype(int)

    # Heavy cloud indicator: 1 if cloud cover is greater than 75%, else 0
    df['is_heavy_clouds'] = (df['clouds_all'] > 75).astype(int)

    # 5. Encode Categorical Weather Variables
    # Apply one-hot encoding to 'weather_main' to produce clean binary columns for the model
    weather_main_encoded = pd.get_dummies(df['weather_main'], prefix='weather', dtype=int)
    df = pd.concat([df, weather_main_encoded], axis=1)

    logger.info("Feature engineering, categorical encoding, and weather indicator creation completed successfully.")
    logger.info(f"New features added. Available columns: {list(df.columns)}")

    # Display a snapshot of the engineered features
    preview_cols = ['date_time', 'hour_sin', 'hour_cos', 'is_weekend', 'is_freezing', 'is_raining', 'is_heavy_clouds'] + list(weather_main_encoded.columns[:3])
    display(df[preview_cols].head())

except Exception as e:
    logger.error("Feature engineering failed.", exc_info=True)

# %%
from sklearn.preprocessing import StandardScaler, MinMaxScaler

try:
    logger.info("--- Scaling and Normalizing Continuous Variables ---")

    # Initialize scalers
    scaler_std = StandardScaler()
    scaler_minmax = MinMaxScaler()

    # 1. Standardize 'temp' (Z-score normalization)
    df['temp_scaled'] = scaler_std.fit_transform(df[['temp']])
    logger.info("Created standardized 'temp_scaled' using StandardScaler.")

    # 2. Min-Max scale 'traffic_volume' (Range [0, 1])
    df['traffic_volume_scaled'] = scaler_minmax.fit_transform(df[['traffic_volume']])
    logger.info("Created normalized 'traffic_volume_scaled' using MinMaxScaler.")

    # Display scaling verification statistics
    display(df[['temp', 'temp_scaled', 'traffic_volume', 'traffic_volume_scaled']].describe())

except Exception as e:
    logger.error("Scaling continuous variables failed.", exc_info=True)

# %% [markdown]
# ### Target Category Engineering: Congestion Levels
# To frame our traffic volume estimation as a classification or categorical analysis task, we define a data-driven **Congestion Category** derived directly from the distribution of `traffic_volume`:
# 
# * **Low Congestion**: Traffic volume is in the bottom 33% quantile (0 to 33rd percentile).
# * **Medium Congestion**: Traffic volume is in the middle quantile (33rd to 66th percentile).
# * **High Congestion**: Traffic volume is in the top 33% quantile (66th to 100th percentile).
# 
# This approach ensures that our categories are balanced and represent statistically significant divisions of the traffic density.

# %%
try:
    logger.info("--- Engineering Congestion Categories ---")

    # Determine the quantile threshold points for 33% and 66%
    q33 = df['traffic_volume'].quantile(0.33)
    q66 = df['traffic_volume'].quantile(0.66)

    logger.info(f"Quantile thresholds calculated: 33rd percentile = {q33:.1f}, 66th percentile = {q66:.1f}")

    # Function to classify traffic volume
    def get_congestion_level(volume):
        if volume <= q33:
            return 'Low'
        elif volume <= q66:
            return 'Medium'
        else:
            return 'High'

    # Map the function to create our categorical target
    df['congestion_category'] = df['traffic_volume'].apply(get_congestion_level)

    # Convert to ordered categorical datatype to preserve hierarchy
    df['congestion_category'] = pd.Categorical(
        df['congestion_category'],
        categories=['Low', 'Medium', 'High'],
        ordered=True
    )

    logger.info("Congestion categories engineered successfully.")

    # Display category distribution metrics to verify balance
    display(df['congestion_category'].value_counts(dropna=False).to_frame())

except Exception as e:
    logger.error("Failed to create congestion categories.", exc_info=True)


