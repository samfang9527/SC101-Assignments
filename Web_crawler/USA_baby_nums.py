"""
File: USA_baby_nums.py
Name: Sam Fang
--------------------------
This file collects data of the number of USA new born babies each years.
Below please see the target url:
https://www.ssa.gov/oact/babynames/decades/names2010s.html
https://www.ssa.gov/oact/babynames/decades/names2000s.html
https://www.ssa.gov/oact/babynames/decades/names1990s.html

You should see:
---------------------------
2010s
Male Number: 10890537
Female Number: 7939153
---------------------------
2000s
Male Number: 12975692
Female Number: 9207577
---------------------------
1990s
Male Number: 14145431
Female Number: 10644002
"""

import requests
from bs4 import BeautifulSoup


def main():
    for year in ['2010s', '2000s', '1990s']:
        print('---------------------------')
        print(year)
        url = 'https://www.ssa.gov/oact/babynames/decades/names'+year+'.html'
        
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, features='html.parser')

        # ----- Write your code below this line ----- #
        items = soup.tbody.find_all('tr')   # [tr1, tr2]
        male_number = 0
        female_number = 0
        for item in items[:-1]:
            td = item.find_all('td')    # [td1, td2]
            male_number += int(remove_comma(td[2].text))
            female_number += int(remove_comma(td[4].text))
        print(f'Male Number: {male_number}')
        print(f'Female Number: {female_number}')


def remove_comma(s):
    """
    param s (str): the string to remove comma.
    """
    new_s = ''
    for ch in s:
        if ch.isdigit():
            new_s += ch
    return new_s


if __name__ == '__main__':
    main()
