
from prophet import Prophet

def train_and_forecast(data, metric_column="metric", periods=7):
    df = data.reset_index()[['timestamp', metric_column]]
    df.columns = ['ds', 'y']

    model = Prophet(daily_seasonality=True)
    model.fit(df)

    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)

    return forecast
