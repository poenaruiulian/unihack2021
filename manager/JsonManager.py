import urllib.request


class JsonManager:
    url = None

    def __init__(self, url):
        self.url = url

    def connect(self):
        fileobj = urllib.request.urlopen(self.url)
        return fileobj.read()
