import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def get_copper_mountain_conditions():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
    driver = webdriver.Chrome(options=chrome_options)

    # Replace this URL with the actual Copper Mountain conditions URL
    url = "https://www.coppercolorado.com/the-mountain/conditions-weather/snow-report"
    driver.get(url)

    # Wait for the page to load (adjust the sleep time if needed)
    driver.implicitly_wait(5)

    # Get the page source after JavaScript execution
    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')

    # Find the elements containing the values
    open_trails_element = soup.find('h3', string='Open Trails')
    open_lifts_element = soup.find('h3', string='Open Lifts')

    # Extract the values
    open_trails_value = extract_value(open_trails_element)
    open_lifts_value = extract_value(open_lifts_element)

    # Define total values
    total_trails = '157'
    total_lifts = '23'

    driver.quit()

    # Format the results and label the report
    copper_mountain_report = (
        f"Copper Mountain\n"
        f"Open Trails: {open_trails_value} of {total_trails}\n"
        f"Open Lifts: {open_lifts_value} of {total_lifts}"
    )

    return copper_mountain_report

def extract_value(element):
    if element:
        # Find the parent li element and extract the text from there
        parent_li = element.find_parent('li', class_='animated')
        if parent_li:
            return parent_li.find_next('text').text.strip()
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

    copper_mountain_report = get_copper_mountain_conditions()

    send_report_to_discord(discord_webhook_url, copper_mountain_report)

    print(copper_mountain_report)
