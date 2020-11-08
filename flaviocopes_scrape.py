""" Scrapper Program to Fetch PDFs from https://flaviocopes.com/ """
# pylint: disable = C0301, W0621
# C0301: Line too long
# W0621: Redefining name from outer scope

import os
import requests
from progressbar import ProgressBar, Bar, Percentage
from bs4 import BeautifulSoup
from format_bytes import format_bytes

def find_urls():
    """ Fetches the List of Ebook's Names and Downloadable URLs from https://flaviocopes.com """
    url = "https://flaviocopes.com/page/list-subscribed/"
    page = BeautifulSoup(requests.Session().get(url).content, "html.parser")
    container = page.find_all("div", {"class": "post-content clearfix"})[0]
    elements = container.find_all("li")
    ebooks = {}
    for element in elements:
        name = element.find_all("strong")[0].text
        link = element.find_all("a")[0]["href"]
        ebooks[name] = link

    return ebooks

def get_ebook(name, url, filesize=0):
    """ Downloads file from PDF page with speed upper limit: 1 MBPS """
    with requests.Session().get(url, stream=True) as request_object:
        size = int(request_object.headers["Content-Length"])
        if size == filesize:
            print(f"File \"{name}\" of size {size} ({format_bytes(size)}) already exists. Skipping download.")
            return 0
        print(f"Writing the file \"{name}\" of size {size} ({format_bytes(size)})")
        request_object.raise_for_status()
        progress_bar = ProgressBar(maxval=(size//(1024*1024)) + 1, widgets=[Bar('=', '[', ']'), ' ', Percentage()])
        progress_bar.start()
        counter = 0
        with open(os.path.join("Exports", name), "wb") as file:
            for chunk in request_object.iter_content(chunk_size=1024*1024):
                file.write(chunk)
                counter += 1
                progress_bar.update(counter)
    progress_bar.finish()
    return 0

if __name__ == "__main__":
    sets = find_urls()
    exists = os.listdir(".\\Exports")
    for name, url in sets.items():
        if name+".pdf" in exists:
            _ = get_ebook(name+".pdf", url, filesize=os.stat(os.path.join("Exports", name+".pdf")).st_size)
        else:
            _ = get_ebook(name+".pdf", url)
        