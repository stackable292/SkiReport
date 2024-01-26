import requests
from bs4 import BeautifulSoup

def get_Arapahoe_Basin_conditions():
    # Replace this URL with the actual Arapahoe Basin conditions URL
    url = "https://www.arapahoebasin.com/snow-report"

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        open_runs = extract_statistic(soup, 'Open Runs')
        open_lifts = extract_statistic(soup, 'Open Lifts')

        return f"**Arapahoe Basin Report**:\nOpen Trails: {open_runs}\nOpen Lifts: {open_lifts}"
    else:
        return f"Failed to retrieve ski conditions. Status code: {response.status_code}"

def extract_statistic(soup, label):
    # Find the p element inside the div with the specified label
    p_element = soup.find('p', string=label)

    if p_element:
        # Find the previous sibling which contains the information
        info_element = p_element.find_previous_sibling('h5')

        if info_element:
            # Replace '/' with ' of '
            info_text = info_element.get_text(strip=True).replace('/', ' of ')
            return info_text

    return f"{label}: N/A"

def send_report_to_discord(webhook_url, report):
    # Create a dictionary with the message content
    data = {
        'content': report
    }

    # Make a POST request to the Discord webhook URL
    response = requests.post(webhook_url, json=data)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print("Report sent to Discord successfully")
    else:
        print(f"Failed to send report to Discord. Status code: {response.status_code}")

if __name__ == "__main__":
    # Replace this with your Discord webhook URL
    discord_webhook_url = "https://discord.com/api/webhooks/1200292789766852638/SL1xXcVP_PJ8UgTpyVvxgOFN0Zbj8H4sroKOoW5sjWdZqGwaswmsK2-iF5oPvoSkRzQX"

    Arapahoe_Basin_report = get_Arapahoe_Basin_conditions()

    # Send the report to Discord
    send_report_to_discord(discord_webhook_url, Arapahoe_Basin_report)

    print(Arapahoe_Basin_report)
