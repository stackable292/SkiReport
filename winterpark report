import requests
from bs4 import BeautifulSoup

def get_winter_park_conditions():
    # Replace this URL with the actual Winter Park Ski Resort conditions URL
    url = "https://www.winterparkresort.com/the-mountain/mountain-report"

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract relevant information
        open_trails = extract_statistic(soup, 'Open Trails')
        open_lifts = extract_statistic(soup, 'Open Lifts')
        
        return f"Open Trails: {open_trails}, Open Lifts: {open_lifts}"
    else:
        return f"Failed to retrieve Winter Park conditions. Status code: {response.status_code}"

def extract_statistic(soup, label):
    statistic_element = soup.find('h6', text=label)
    if statistic_element:
        # Traverse up the DOM tree to find the parent div containing the statistic
        parent_div = statistic_element.find_parent('div', class_='StatsWidget_statistic__IMiZE')
        statistic = parent_div.find('span', class_='StatsWidget_statBig__JTduy').text.strip()
        return statistic
    else:
        return 'N/A'

def send_report_to_discord(webhook_url, report):
    data = {
        "content": report
    }
    response = requests.post(webhook_url, json=data)

    if response.status_code == 204:
        print("Report sent to Discord successfully!")
    else:
        print(f"Failed to send report to Discord. Status code: {response.status_code}")

if __name__ == "__main__":
    # Replace this with your Discord webhook URL
    discord_webhook_url = "https://discord.com/api/webhooks/1187184664138489856/2AhHO2fdZdcTsEBk7KXJxLSJfWIsrEVmxtHBoqvP3FHNCppe3N0PzPprNRn0d3odVKMW"

    winter_park_report = get_winter_park_conditions()

    # Send the report to Discord
    send_report_to_discord(discord_webhook_url, winter_park_report)
