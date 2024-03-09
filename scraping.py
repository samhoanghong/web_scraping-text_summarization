import requests
from bs4 import BeautifulSoup
import yaml
from extract_url import extract_url


def extract_content(url):

    print(url)

    with open('exclude_config.yaml', 'r') as f:
        classes = yaml.full_load(f)
        exclude_classes = classes['exclude_classes']
        exclude_footer = classes['exclude_div_footer']
    try:
        response = requests.get(url, timeout=10)
    except:
        print("Can't connect to the news page!!!!")
        return None
    
    html_source = response.text

    soup = BeautifulSoup(html_source, 'html.parser')

    with open ('textfiles/cont.txt', 'w') as f:
        f.write(str(soup))

    exclude_tags = soup.find_all('p', class_=exclude_classes)

    for exclude_tag in exclude_tags:
        exclude_tag.extract()

    #exclude footer
    exclude_tags = soup.find_all('div', class_=exclude_footer)
    for exclude_tag in exclude_tags:
       exclude_tag.extract()

    exclude_tags = soup.find_all('footer')
    for exclude_tag in exclude_tags:
       exclude_tag.extract()

    paragraph_tags = soup.find_all("p")

    clean = []

    for paragraph_tag in paragraph_tags:

        paragraph_text = paragraph_tag.get_text()
        clean.append(paragraph_text)
        #print(paragraph_text)

    

    full_text = ""
    with open("textfiles/pagecontent.txt", "w") as f:
        for sen in clean:
            f.write(sen + "\n")
            full_text += sen
    # for sen in clean:
    #     full_text += sen
    return full_text

# extract_content('https://calgary.ctvnews.ca/house-destroyed-in-sunday-morning-fire-in-southeast-calgary-1.6792911')
extract_content(extract_url("computer"))
