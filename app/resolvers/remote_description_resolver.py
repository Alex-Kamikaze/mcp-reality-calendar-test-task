import requests
from bs4 import BeautifulSoup
from exceptions.remote_resolver_exceptions import ResolvingException

class RemoteProductDescriptionResolver:

    def get_product_description_from_link(self, link: str) -> str:
        resp = requests.get(link, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"})
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            for script in soup(["script", "style"]):
                script.decompose()
            
            return soup.get_text(separator=" ", strip=True)
        else:
            print(resp.status_code)
            print(resp.text)
            raise ResolvingException()