from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import requests

def get_winter_park_conditions():
    # Replace this URL with the actual Winter Park Ski Resort conditions URL
    url = "https://www.winterparkresort.com/the-mountain/mountain-report"

    # Configure ChromeOptions to run headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Start the WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Open the URL in the headless browser
        driver.get(url)

        # Wait for the page to load (adjust the sleep time if needed)
        time.sleep(5)

        # Extract and display all statistics
        statistics = extract_statistics(driver.page_source)
        return statistics
    finally:
        # Close the WebDriver
        driver.quit()

def extract_statistics(html):
    # Parse the HTML content
    soup = BeautifulSoup(html, 'html.parser')

    # Find the element with class 'StatsWidget_statsList__e9aIo'
    stats_list = soup.find('div', class_='StatsWidget_component__VLUsC')

    if stats_list:
        # Find all 'li' elements within the stats list excluding "Mountain Activities" and "Open Terrain"
        stat_items = [item for item in stats_list.find_all('li', class_='StatsWidget_statItem__yJzYz') if 'Mountain Activities' not in item.text and 'Open Terrain' not in item.text]

        # Static total counts
        static_total_trails = 171
        static_total_lifts = 24

        # Initialize a list to store formatted statistics
        formatted_statistics = []

        for item in stat_items:
            # Find the label and statistic within each 'li' element
            label = item.find('h6').text.strip()
            statistic = item.find('span', class_='StatsWidget_statBig__JTduy').text.strip()

            if label == 'Open Trails':
                formatted_statistics.append(f"{label}: {statistic} of {static_total_trails}")
            elif label == 'Open Lifts':
                formatted_statistics.append(f"{label}: {statistic} of {static_total_lifts}")
            else:
                formatted_statistics.append(f"{label}: {statistic}")

        # Additional search for "Last 24 Hour"
        last_24_hours_element = soup.find('p', class_='LabeledItem_component__hgsZz', string='Last 24 Hour:')
        if last_24_hours_element:
            last_24_hours_statistic = last_24_hours_element.find('strong').text.strip()
            formatted_statistics.append(f"Last 24 Hours: {last_24_hours_statistic}")

        return formatted_statistics
    else:
        return []

# Rest of the code remains unchanged


def send_report_to_discord(webhook_url, report):
    data = {
        'content': report
    }

    response = requests.post(webhook_url, json=data)

    if response.status_code == 204:
        print("Report sent to Discord successfully")
    else:
        print(f"Failed to send report to Discord. Status code: {response.status_code}")

if __name__ == "__main__":
    discord_webhook_url = "https://discord.com/api/webhooks/1200292789766852638/SL1xXcVP_PJ8UgTpyVvxgOFN0Zbj8H4sroKOoW5sjWdZqGwaswmsK2-iF5oPvoSkRzQX"

    winter_park_report = get_winter_park_conditions()

    # Format the report without "CO Snow Report," "Mountain Activities," and "Open Terrain"
    # Display "Winter Park" above the results without an extra line
    formatted_report = f"**Winter Park Report**\n{'\n'.join(winter_park_report)}"
    print(formatted_report)

    send_report_to_discord(discord_webhook_url, formatted_report)
