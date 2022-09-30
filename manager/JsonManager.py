from urllib.request import Request, urlopen


class JsonManager:
    url = None

    def __init__(self, url):
        self.url = url

    def connect(self):
        fileobj = Request(self.url, headers={"User-Agent":"Chrome/106.0.0.0"})
        return urlopen(fileobj).read()  
