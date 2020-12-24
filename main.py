import datetime

now = datetime.datetime.now()
year = now.year
print(f'Year->{year}')

dl_folder = 'dl'


def dl(search):
    import sys
    import os.path
    import requests
    from bs4 import BeautifulSoup
    from pathlib import Path

    import re

    Path(f'{dl_folder}/{search}').mkdir(parents=True, exist_ok=True)

    search_text = requests.get(f'https://magazinelib.com/?s={search}').text
    for link in BeautifulSoup(search_text, 'html.parser').find_all('a', rel="bookmark"):
        dl_link = link.get('href')
        dl_text = requests.get(dl_link).text
        file_link = BeautifulSoup(dl_text, 'html.parser').find('a', target="_blank")
        file_url = file_link.get('href')
        file_name = file_link.get_text()

        path = f'{dl_folder}/{search}/{file_name}'

        if re.search(f'[{str(year)}|{str(year+1)}]', file_name) is not None or not os.path.isfile(path):
            file_req = requests.get(file_url, allow_redirects=True)
            # print(f'file_req-> {file_req}')
            file_size = len(file_req.content)
            print(f'dl-ing {file_name} {file_size}bytes')
            if file_size > 500_000:
                open(path, 'wb').write(file_req.content)
                print(f'dl-ed {file_name}')
                # sys.exit()
            else:
                print(f'skipped {file_name} as too small')
        else:
            print(f'skipped {file_name} as already dl-ed or expired')


if __name__ == '__main__':
    # dl('economist')
    dl('kiplinger')
    # dl('finweek')
    # dl('bloomberg')
    # dl('harvard')
    # dl('linux')
    # dl('barron')
    # dl('market watch')
    # dl('new york times')

