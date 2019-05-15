from bs4 import BeautifulSoup
import csv
import requests 
import time

# set filename
filename = ""
#set start and end page range
start = 0
end = 10

start = time.time()
url = "https://www.presidency.ucsb.edu/advanced-search?field-keywords=&field-keywords2=&field-keywords3=&from%5Bdate%5D=&to%5Bdate%5D=&person2=200300&items_per_page=100&page="
doc = open(filename, 'w')
f = csv.writer(doc)   # Open the output file for writing before the loop
f.writerow(["Date", "Title", "Text", "Link"]) 
for i in range(start, end):
    new_url = url + str(i)
    response = requests.get(new_url)
    soup = BeautifulSoup(response.content, "html.parser")
    final_link = soup.p.a
    final_link.decompose()
    trs = soup.find_all('tr')
    for tr in trs:
        for link in tr.find_all('a'):
            full = link.get('href')
            if str.startswith(full, "/documents"):
                fulllink = "https://www.presidency.ucsb.edu" + full
                #print(fulllink)
        tds = tr.find_all("td")
        try: 
            page_response = requests.get(fulllink)
            page_content = BeautifulSoup(page_response.content, "html.parser")
            name_box = page_content.find("div", attrs={"class": "field-docs-content"})
            text = name_box.text.strip()
            #print(text)
            title_box = page_content.find("div", attrs={"class", "field-ds-doc-title"})
            title = title_box.text.strip()    
            #print(title)
            date_box = page_content.find("span", attrs={"class", "date-display-single"})
            date = date_box.text.strip()
            #print(date)
        except:
            continue    
        try:
            f.writerow([date, title, text, fulllink])
        except:
            continue
end = time.time()
doc.close()
print(end-start)