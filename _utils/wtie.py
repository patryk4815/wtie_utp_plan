from bs4 import BeautifulSoup


def get_informatyka_href(text_data):
    soup = BeautifulSoup(text_data, "html5lib")
    for elem in soup.find_all('h2'):
        if elem.text.find('Informatyka stosowana') != -1:
            for elem2 in elem.next_elements:
                if elem2.name == 'h2':
                    break

                try:
                    elem2_text = elem2.text
                except AttributeError:
                    continue

                if (
                    elem2_text.find('Studia niestacjonarne I stopnia') != -1 and
                    elem2_text.find('II Semestr') != -1
                ):
                    return elem2.find('a').get('href')

    return None
