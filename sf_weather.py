from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pandas  as pds

page = requests.get("http://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168")
soup = BeautifulSoup(page.content,"html.parser")
seven_day=soup.find(id="seven-day-forecast")

forecast_items=seven_day.find_all(class_="tombstone-container")


period_tags=seven_day.select(".tombstone-container .period-name")
periods=[pt.get_text() for pt in period_tags]

short_descs=[sd.get_text() for sd in seven_day.select(".tombstone-container .short-desc")]
temps = [t.get_text() for t in seven_day.select(".tombstone-container .temp")]
descs = [d["title"] for d in seven_day.select(".tombstone-container img")]

weather=pds.DataFrame({
    "period":periods,
    "short_desc": short_descs, 
    "tempe": temps, 
    "descr":descs})

temp_nums=weather["temp"].str.extract("(?P<temp_num>\d+)", expand=False)
weather["temp_num"]=temp_nums.astype("int")

temp_cel=[(tmp-32)/1.8 for tmp in weather["temp_num"]]
temp_cel
weather["temp_cel"]=temp_cel

weather.to_excel("sf_weather.xlsx")