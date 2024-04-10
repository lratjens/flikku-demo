import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_script(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            script_tag = soup.find('pre')
            return script_tag.get_text() if script_tag else "Script not found"
        else:
            return "Failed to access URL"
    except Exception as e:
        return f"Error: {e}"


def get_scripts():
    urls = [
        "https://imsdb.com/scripts/Tenet.html"
        ,"https://imsdb.com/scripts/Top-Gun.html"
        ,"https://imsdb.com/scripts/Bad-Boys.html"
        ,"https://imsdb.com/scripts/Ocean's-Eleven.html"
        ,"https://imsdb.com/scripts/Aladdin.html"
        ,"https://imsdb.com/scripts/Kung-Fu-Panda.html"
        ,"https://imsdb.com/scripts/Jaws.html"
        ,"https://imsdb.com/scripts/American-Psycho.html"
        ,"https://imsdb.com/scripts/Shrek.html"
        ,"https://imsdb.com/scripts/Sex-and-the-City.html"
        ,"https://imsdb.com/scripts/Die-Hard.html"
        ,"https://imsdb.com/scripts/A-Few-Good-Men.html"
        ,"https://imsdb.com/scripts/Avatar.html"
        ,"https://imsdb.com/scripts/Avengers-Endgame.html"
        ,"https://imsdb.com/scripts/Wall-Street.html"
        ,"https://imsdb.com/scripts/Sherlock-Holmes.html"
        ,"https://imsdb.com/scripts/Truman-Show,-The.html"
        ,"https://imsdb.com/scripts/Ghostbusters.html"
        ,"https://imsdb.com/scripts/La-La-Land.html"
        ,"https://imsdb.com/scripts/Jurassic-Park-The-Lost-World.html"
        ,"https://imsdb.com/scripts/Armageddon.html"
        ,"https://imsdb.com/scripts/Platoon.html"
        ,"https://imsdb.com/scripts/Saving-Private-Ryan.html"
        ,"https://imsdb.com/scripts/Wall-E.html"
        ,"https://imsdb.com/scripts/Django-Unchained.html"
        ,"https://imsdb.com/scripts/12-Years-a-Slave.html"
        ,"https://imsdb.com/scripts/Sixth-Sense,-The.html"
        ,"https://imsdb.com/scripts/Bourne-Identity,-The.html"
    ]
    # scripts = {url.split('/')[-1].split('.')[0]: scrape_script(url) for url in urls}
    # return scripts
    records = []
    for url in urls:
        title = url.split('/')[-1].split('.')[0]
        script_text = scrape_script(url)
        records.append({'title': title, 'url': url, 'script': script_text})
    scripts_df = pd.DataFrame(records, columns=['title', 'url', 'script'])
    return scripts_df

