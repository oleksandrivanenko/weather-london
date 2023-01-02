import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

# Get weather data from the site
URL = "https://weather.com/weather/tenday/l/1db42e1c2cd5058c3286bd2c319d07f0b10277bb47218b7361a458f2c07b2975"
weather_site = requests.get(URL)
soup = BeautifulSoup(weather_site.content, "lxml")
weather_data_list = []
for x in range(1, 15):
    day = soup.select(".DetailsSummary--daypartName--kbngc")[x].get_text()
    high = round(((int(soup.select(".DetailsSummary--highTempValue--3PjlX")[x].get_text()[0:2])) - 32) / 1.8)
    low = round(((int(soup.select(".DetailsSummary--lowTempValue--2tesQ")[x].get_text()[0:2])) - 32) / 1.8)
    weather_data_list.append([day, high, low])

# Сreate a CSV file to save data from the site
weather_data = pd.DataFrame(weather_data_list, columns=["Day", "High", "Low"])
weather_data.to_csv("weather_data_london_14days.csv")

# Create a graph for the data
days = [day for day in weather_data["Day"]]
high = [high for high in weather_data["High"]]
low = [low for low in weather_data["Low"]]
plt.figure(figsize=(12,9))
plt.plot(days, high, marker="o", color="orange", label="High")
plt.plot(days, low, marker="o", color="blue", label="Low")
plt.title(f"London ({days[0]} - {days[-1]})")
plt.xlabel ("Day")
plt.ylabel ("Degrees(°C)")
plt.xticks(rotation="vertical")
plt.yticks ([x for x in range(0,16)])
plt.grid()
plt.legend()
plt.savefig("weather_graph.png", dpi=300)
plt.show()