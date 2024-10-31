import requests


def runPowerLodger():
    # URL to scrape
    url = "https://www.powerlodgeramsey.com/search/inventory/availability/In%20Stock/sort/discount/type/Pontoons/type/Boats/usage/New/page/1"

    # Send a GET request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors

    # Write the HTML response to a text file
    with open("response_page.txt", "w", encoding="utf-8") as file:
        file.write(response.text)

    print("Response has been written to response_page.txt")
