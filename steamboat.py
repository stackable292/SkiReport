import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def get_steamboat_conditions():
    # Replace this URL with the actual Steamboat Ski Resort conditions URL
    url = "https://www.steamboat.com/the-mountain/mountain-report"

    # Configure ChromeOptions to run headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Start the WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Open the URL in the headless browser
        driver.get(url)

        # Wait for the page to load (adjust the sleep time if needed)
        driver.implicitly_wait(10)

        # Extract and display the number of open trails, open lifts, total trails, and total lifts
        open_trails = extract_statistic(driver.page_source, 'Open Trails')
        open_lifts = extract_statistic(driver.page_source, 'Open Lifts')
        total_trails = 181  # Static value
        total_lifts = 23  # Static value

        steamboat_report = (
            f"Steamboat Report:\n"
            f"Open Trails: {open_trails.replace('/', ' of ')} / {total_trails}\n"
            f"Open Lifts: {open_lifts.replace('/', ' of ')} / {total_lifts}"
        )

        return steamboat_report
    finally:
        # Close the WebDriver
        driver.quit()

def extract_statistic(html, label):
    # Parse the HTML content
    soup = BeautifulSoup(html, 'html.parser')

    # Find the 'h6' element with the label
    h6_element = soup.find('h6', string=lambda s: s and label in s)

    if h6_element:
        # Find the closest 'li' parent
        parent_li = h6_element.find_parent('li', class_='StatsWidget_statItem__yJzYz')

        if parent_li:
            # Find the 'span' element with the number
            statistic = parent_li.find('span', class_='StatsWidget_statBig__JTduy')
            if statistic:
                return statistic.text.strip()

    # If the label is not found in the usual structure, try to find it in the entire page
    label_element = soup.find('h6', string=label)
    if label_element:
        # Find the closest 'div' parent
        parent_div = label_element.find_parent('div', class_='StatsWidget_statistic__IMiZE')
        if parent_div:
            # Find the next 'span' element with the number
            statistic = parent_div.find_next('span', class_='StatsWidget_statBig__JTduy')
            return statistic.text.strip() if statistic else 'N/A'

    return 'N/A'

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
    discord_webhook_url = "https://discord.com/api/webhooks/1187184664138489856/2AhHO2fdZdcTsEBk7KXJxLSJfWIsrEVmxtHBoqvP3FHNCppe3N0PzPprNRn0d3odVKMW"

    steamboat_report = get_steamboat_conditions()

    send_report_to_discord(discord_webhook_url, steamboat_report)

    print(steamboat_report)