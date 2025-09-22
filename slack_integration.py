import requests

 

def send_to_slack(message):
    url = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization": f"Bearer {SLACK_TOKEN}"}
    data = {"channel": CHANNEL_ID, "text": message}
    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200 or not response.json().get("ok"):
        print("Error sending to Slack:", response.json())
    else:
        print("Alert sent to Slack!")
