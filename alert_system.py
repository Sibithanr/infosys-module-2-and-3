def check_alerts(data, forecast, metric_column="metric"):
    alerts = []

    latest_value = data[metric_column].iloc[-1]
    forecast_next = forecast['yhat'].iloc[-1]

    if latest_value < forecast_next * 0.8:
        alerts.append(f"Drop detected in {metric_column}! Actual={latest_value}, Expected={forecast_next:.2f}")

    return alerts
