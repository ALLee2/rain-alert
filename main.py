import requests
import os
# from twilio.rest import Client
# from twilio.http.http_client import TwilioHttpClient
import smtplib

# OWM == Open Weather Map
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
MY_LAT = os.environ["MY_LAT"]
MY_LON = os.environ["MY_LON"]
api_key = os.environ["api_key"]
# account_sid = os.environ["account_sid"]
# auth_token = os.environ["auth_token"]
my_email = os.environ["my_email"]
my_password = os.environ["my_password"]

weather_parameters = {
    "lat": MY_LAT,
    "lon": MY_LON,
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

response = requests.get(url=OWM_Endpoint, params=weather_parameters)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    # proxy_client = TwilioHttpClient()
    # proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    #
    # client = Client(account_sid, auth_token, http_client=proxy_client)
    # message = client.messages \
    #     .create(
    #     body="It's going to rain today. Remember to bring an ☔",
    #     from_="YOUR TWILIO VIRTUAL NUMBER",
    #     to="YOUR TWILIO VERIFIED REAL NUMBER"
    # )
    # print(message.status)
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=my_email, password=my_password)
    connection.sendmail(from_addr=my_email,
                        to_addrs=os.environ["to_addrs"],
                        msg="Subject:Weather Alert!\n\nIt's going to rain today. Remember to bring an umbrella!"
                        )
