import time
import requests
import json
#import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime

api_key = "615dec1abdd2d864b941c12a3b2236ef7531ea48fece4b52ac87152b781cb19f"
trend = "gainers"  # Specify the trend parameter (e.g., "gainers" or "losers")
url = f"https://serpapi.com/search?engine=google_finance_markets&trend={trend}&api_key={api_key}"

# Make the request with a 5-second delay
response = requests.get(url)
time.sleep(5)

data = response.json()

# Extract relevant information directly without saving to JSON file
market_trends = data.get("market_trends", [])
stocks = []
names = []
prices = []
percentages = []

for trend in market_trends:
    results = trend.get("results", [])
    for result in results:
        stock_full = result.get("stock")
        stock = stock_full.split(":")[0] if ":" in stock_full else stock_full
        name = result.get("name")
        price = result.get("extracted_price")
        percentage = result.get("price_movement", {}).get("percentage")
        if stock and name and price and percentage:
            stocks.append(stock)
            names.append(name)
            prices.append(price)
            percentages.append(float(percentage) / 100)  # Divide by 100 to convert percentage to decimal

# Create DataFrame
df = pd.DataFrame({'Stock': stocks, 'Name': names, 'Price': prices, 'Percentage': percentages})

# Add date stamp
date_stamp = datetime.now().strftime("%Y-%m-%d")
df["Date"] = date_stamp

# Credentials dictionary
credentials_dict = {
  "type": "service_account",
  "project_id": "stocks-414522",
  "private_key_id": "ff3fe1acc48b0e11cfe40da15d21113beb7adac5",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCwl3BXHaTGIPyP\nel+zE+S1lIrC8V02NGqrVj7xL6z4BuC8bMQKlu+nUnTTzDN/A3JzRtYOlzs44WqQ\ndhFAxaVSUfWb6zqXwUk3CVi9SOjVJsUTvds7/uDjTmFasSBHPZQcWqDWkqrGt7A2\n+WJ43gwv/B9Cloadh06k4r/3EV3f8U/xhLA3U5o7s2pSj/dIRVVAgPKlCl3u/urx\nro6U/aoa0ifuoj9Qpd2ksHOwKPIX4ruqmmaj10gPK7MBjsloOenlVhocckkPLn0/\ny5UTNT/DTuV4e3Idpiy7hDT/GnxwMJ4CmsWrdGDj42tQ/Jo5YwkhIUK4kG9jIz1T\nUChFBJcLAgMBAAECggEABgyZ/5H3ZAYbQLr7bkH/Mq0s97KW89Vl1gq1S0PL1A9A\nQZQkPwyelwe/EsZK+U3f7Mz/Zi6OC8vE/7/bpXFf0WsXU8kCD9LCNE1wqcNGno6e\nb6ewS+TWRVMZCKdKqMYWPcZo/hC2IuqF8cwnMGbC2h3z4C8R23GYIxPVaZxBr/sg\nn1ctoiboouZv/HFFZ+6Ax+oDwkNYZWwwPeJy32R/2YSJS2B3ZqNwS3JeWA7IEp3C\nlLPMcRTXD/mo23Mni/DdMrp1rt8QYeq6GDosVS6SmfRS9SNwrMeYp8737Ye3fmOK\nrOA1ZYS8kzgMh4JD3CBnKU+jhO0f69AcO5xdcY924QKBgQDhe/eo0nAD/40LabEn\n/8YkYgKH8u2X7MeuLL0ZeQgt1E6Nokwc2eswfsk5X1/eTyzGJ7dEKicQOF0b18a0\n5QD5luDordcnt2cXB0z9YZfG5DTzqQg1P14KBaOlNq9ToCP6I3SzAGZptRIkyVTd\nZYXnLAu+OPvDoPZjX9k3bsDAcQKBgQDIfY5JRDbaj7nwp7qt2VOp7DNr6x25fd94\nvctmE0AIwok2ME/jZICkYXdF5eyGrp3gP636zmGiXYJvz1p/HvEyfbSpWuhM56x8\nk3X58rza/gMl++CAPFOaZaRiHRH7/IR6xdjXvsRKbkL+SNj1ABPy5SR5mdk4mBgX\nrHgTKzqNOwKBgDKEjrERLK2IpLYI4PsAMAlYuA5zW83s67PXLCq31iBGb68FzJ2u\nKSY9UaH7/0OUY4ilv0aTVxsoNZwWVNuUbwp8Rjl7MTghvAQJy7L9GX8jA8YPedpM\nLyp5pvdN8CwBNe5F4VB1Z3yJZ948CTptE3n+gUcGB0oGFw2enNDxjFfRAoGBAKac\n6OTsQmWpsY1T5mhZRhTdTPJvRpmDCHavy1t9veZJvHuC9LD1MY7pzJQS+lgGvv7A\nDNZ0MmEbMq22dO9ViH48RynCeXCHyykP5qgb2GRpWbZ0NmJ7P8L8mvpKTErL1FCv\nIIBScY+lSBlH8rzQHsPpN0Gy3/kPNF5gHr1XXGZHAoGAUS6Gg1k1sQ0exrWC7NAr\nslvR/eD2c2eK8wwxEuXtgfjT3qjjHAkWgRIOVX5MCLCo8qp9Ytsk9RxAVFIwsT/u\n3TydLt+iDRr8mNXim/dGPhKv7Qrgo7ALTzkdmluar2XSi76e//iPeA1JiXiTf24H\nKlI3XWfrH7PteQ0rpCC7zYI=\n-----END PRIVATE KEY-----\n",
  "client_email": "stocks@stocks-414522.iam.gserviceaccount.com",
  "client_id": "117686476662700380803",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/stocks%40stocks-414522.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# Authenticate with Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
client = gspread.authorize(credentials)

# Open the Google Sheets file by its document ID
doc_id = "149fE-wlDHqE25k3g2mzaKVJG6XD95BY44grTxGMt3wc"  # Replace with the actual document ID
sheet = client.open_by_key(doc_id).sheet1

# Convert DataFrame to a list of lists and append to Google Sheets
data_to_append = df.values.tolist()
sheet.append_rows(data_to_append)

print("Data has been successfully written to Google Sheets.")
