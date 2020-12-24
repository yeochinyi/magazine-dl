# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys
import os.path

dl_folder = 'dl'



def dl(search):
    import requests
    from bs4 import BeautifulSoup

    search_text = requests.get(f'https://magazinelib.com/?s={search}').text
    for link in BeautifulSoup(search_text, 'html.parser').find_all('a', rel="bookmark"):
        dl_link = link.get('href')
        dl_text = requests.get(dl_link).text
        file_link = BeautifulSoup(dl_text, 'html.parser').find('a', target="_blank")
        file_url = file_link.get('href')
        file_name = file_link.get_text()

        path = f'{dl_folder}/{search}/{file_name}'
        if not os.path.isfile(path):
            file_req = requests.get(file_url, allow_redirects=True)
            print(f'file_req-> {file_req}')
            if len(file_req.content) > 100_000:
                open(path, 'wb').write(file_req.content)
                print(f'dl-ed {file_name}')
                sys.exit()
            else:
                print(f'skipped {file_name} as too small')
        else:
            print(f'skipped {file_name} as already dl-ed')


if __name__ == '__main__':
    # dl('economist')
    # dl('kiplinger')
    dl('finweek')
    # dl('bloomberg')
    # dl('harvard')

