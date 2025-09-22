import pandas as pd

def load_and_clean_data(file_path="realtime_news.csv", metric_column="keyword_count"):
    data = pd.read_csv(file_path)

    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data = data.set_index('timestamp').sort_index()

    if len(data) < 2:
        print("⚠️ Not enough data, skipping resampling")
        return data

    data = data.asfreq('D')
    data[metric_column] = data[metric_column].interpolate()

    return data
