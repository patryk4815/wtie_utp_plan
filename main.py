import time
import requests
from pathlib import Path

from _utils.mail import send_email
from _utils.pdf import diff_pdf_pages
from _utils.wtie import get_informatyka_href


def main():
    # pobranie html strony z planami lekcji
    data = requests.get('http://wtie.utp.edu.pl/', params={
        'page_id': '88',
    })
    if data.status_code != 200:
        exit(2)

    # pobranie linku do pdf z planem
    pdf_url = get_informatyka_href(data.text)
    if pdf_url is None:
        exit(3)

    # pobranie pliku pdf z planem
    pdf_data = requests.get(pdf_url)
    if pdf_data.status_code != 200:
        exit(4)
    pdf_bytes = pdf_data.content

    # tutaj jest magja, tworzenie katalogu tmp w katalogu domowym
    # zeby moc porownac sobie poprzednie pdfy czy sie zmienily
    tmp_dir_pdf = Path.home() / Path('.pdf_tmp')
    if not tmp_dir_pdf.exists():
        tmp_dir_pdf.mkdir()

    # pobieranie ostatniego pliku z katalogu tmp
    list_files = [(int(o.name.split('.')[0]), o) for o in tmp_dir_pdf.iterdir()]
    list_files.sort(key=lambda x: x[0], reverse=True)
    if list_files:
        last_file = list_files[0][1]
        last_bytes = last_file.open('rb').read()
    else:
        last_file = None
        last_bytes = b''

    # dodanie pdf do katalogu i usuniecie poprzedniego pliku
    new_file = tmp_dir_pdf / Path('{}.pdf'.format(int(time.time())))
    new_file.open('wb').write(pdf_bytes)
    if last_file:
        last_file.unlink()

    # sprawdzanie czy byly zmiany w pdf
    page_change = diff_pdf_pages(last_bytes, pdf_bytes)
    if not page_change:
        exit(5)

    # gdy byly zmiany to wysylamy email sobie na poczte :)
    title = 'ZMIANA PLANU ZAJEC STUDIA'
    msg = 'ZMIANA PLANU ZAJEC STUDIA, str: {}'.format(page_change)
    send_email(title, msg, 'bux.patryk@gmail.com', 'noreply@cypis.ovh')


if __name__ == '__main__':
    main()
