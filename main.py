import requests
from bs4 import BeautifulSoup


def get_content(pg=1171355):
    url = f"http://www.shuyyw.cc/read/1102/{pg}.html"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    header = soup.find("h1").text
    header = header[header.index('正文')+3:]
    print(header)
    year_context = soup.find(attrs={"id": "content"}).contents

    join = '\n\n'.join(filter(lambda i: i != "", map(lambda x: x.text, year_context)))
    join = join[:join.index("〖")]
    print(join)


if __name__ == "__main__":
    get_content()
