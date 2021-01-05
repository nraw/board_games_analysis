import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from time import sleep


def get_geeklist(geeklist_id):
    geeklist_url = f"https://www.boardgamegeek.com/xmlapi/geeklist/{geeklist_id}"

    res = requests.get(geeklist_url)
    xml_content = res.content
    bs = BeautifulSoup(xml_content, "lxml")
    items = bs.find_all("item")
    geeklist = [item.get("objectid") for item in items]
    return geeklist


if __name__ == "__main__":
    geeklist_id = "244099"  # susd
    geeklist_id = "265480"  # dice tower excellence
    geeklist_id = "252354"  # BGA
    geeklist = get_geeklist(geeklist_id)

