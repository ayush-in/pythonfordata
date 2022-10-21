import requests
from bs4 import BeautifulSoup
import csv

url = "https://en.wikipedia.org/wiki/Maroon_5_discography"
r = requests.get(url)

# cont = r.content
# print(cont)


soup = BeautifulSoup(r.content, 'html.parser')
# print(soup.prettify())

table = soup.find('table', class_="wikitable plainrowheaders")
#print(table)


anchors = table.findAll('a')
# print(anchors)
l = []
for link in anchors:
    if 'album' in link['href'] and '#' not in link['href']:
        a = "https://en.wikipedia.org//" + link.get('href')
        l.append(a)
        # print(link['href'])
print(l)


# anchors = soup.findAll('a')
# full_link = set()
# for link in anchors:
#     print(link.get('href'))
#     if link.get('href') != '#' or link.get('href') != None:
#         linktext = "https://en.wikipedia.org//" + link.get('href')
#         full_link.add(linktext)
#         print(full_link)

for link in l:
    songs = []
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('table', class_="tracklist")
    tr_tag2 = table.find_all("tr")[1:-1]
    result = {}

    for tag in tr_tag2:
        title = tag.find("td")
        duration = tag.find("td", class_="tracklist-length")
        result = {"title": title.text.replace("\"", ""), "duration": duration.text}
        songs.append(result)


    with open(link[32:] + ".csv", "w") as csv_file:
        col_name = ["title", "duration"]
        writer = csv.DictWriter(csv_file, fieldnames=col_name)
        writer.writeheader()
        for song in songs:
            writer.writerow(song)

print(songs)



