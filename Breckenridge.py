import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession

def get_Breckenridge_conditions():
    url = "https://www.breckenridge.com/the-mountain/mountain-conditions/terrain-and-lift-status.aspx"

    session = HTMLSession()
    response = session.get(url)

    if response.status_code == 200:
        response.html.render()

        breckenridge_report = "**Breckenridge Report**\n"

        trail_info = response.html.find('.terrain_summary__tab_main__text:contains("trails Open")', first=True)
        if trail_info:
            trails_open = trail_info.find('.c118__number1--v1', first=True)
            total_trails = trail_info.find('.c118__number2--v1', first=True)
            breckenridge_report += f"Open Trails: {trails_open.text} of {total_trails.text.replace('/', '')}\n"

        lift_info = response.html.find('.terrain_summary__tab_main__text:contains("Lifts Open")', first=True)
        if lift_info:
            lifts_open = lift_info.find('.c118__number1--v1', first=True)
            total_lifts = lift_info.find('.c118__number2--v1', first=True)
            breckenridge_report += f"Open Lifts: {lifts_open.text} of {total_lifts.text.replace('/', '')}\n"

        

        if not lift_info and not trail_info:
            breckenridge_report += "No information found on the page."

        return breckenridge_report
    else:
        return f"Failed to retrieve the page. Status code: {response.status_code}"

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

    breckenridge_report = get_Breckenridge_conditions()

    send_report_to_discord(discord_webhook_url, breckenridge_report)

    print(breckenridge_report)
