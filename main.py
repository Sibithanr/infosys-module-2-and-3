import os
from data_processing import load_and_clean_data
from forecasting_model import train_and_forecast
from alert_system import check_alerts
from slack_integration import send_to_slack

def main():
    if os.path.exists("realtime_news.csv"):
        file_path = "realtime_news.csv"
        metric_column = "keyword_count"   
    else:
        file_path = "historical_data.csv"
        metric_column = "metric"

    data = load_and_clean_data(file_path=file_path, metric_column=metric_column)

    forecast = train_and_forecast(data, metric_column=metric_column)
    alerts = check_alerts(data, forecast, metric_column=metric_column)

    for alert in alerts:
        send_to_slack(alert)

    print("Alerts processed.")

if __name__ == "__main__":
    main()
send_to_slack("Test alert: Slack integration working!")
