import requests
import fake_useragent
from bs4 import BeautifulSoup

from find_number import find_number
from translate import translate

URL = 'https://brest.rabota.by/search/vacancy'

def get_amount_of_pages(desired_job,  type_of_years_of_experience, type_of_work, salary, without_salary) -> int:
    user_agent = fake_useragent.UserAgent().random
    header = {'user-agent': user_agent}

    params = {
        'area': 16,
        'text': desired_job,
        'page': 0,
        'items_on_page': 20,
        'salary_mode': type_of_work,
        'salary': salary,
        'experience': type_of_years_of_experience,
        'search_period': 0,
        'search_field': 'name'
    }
    if not without_salary:
        params['label'] = 'with_salary'

    response = requests.get(URL, params=params, headers=header)
    soup = BeautifulSoup(response.text, "lxml")

    amount_of_vacancies = find_number(soup.find("h1", class_='magritte-text___gMq2l_7-0-2 magritte-text-overflow___UBrTV_7-0-2 magritte-text-typography-small___QbQNX_7-0-2 magritte-text-style-primary___8SAJp_7-0-2').text)
    amount_of_pages = (amount_of_vacancies + 19) // 20

    return amount_of_pages

def get(cur_language, desired_job, desired_city, type_of_years_of_experience, type_of_work, salary, without_salary) -> list:
    user_agent = fake_useragent.UserAgent().random
    header = {'user-agent': user_agent}

    res = []

    amount_of_pages = get_amount_of_pages(desired_job,  type_of_years_of_experience, type_of_work, salary, without_salary)
    for page in range(amount_of_pages):
        params = {
            'area': 16,
            'text': desired_job,
            'page': page,
            'items_on_page': 20,
            'salary_mode': type_of_work,
            'salary': salary,
            'experience': type_of_years_of_experience,
            'search_period': 0,
            'search_field': 'name'
        }
        if not without_salary:
            params['label'] = 'with_salary'

        response = requests.get(URL, params=params, headers=header)
        soup = BeautifulSoup(response.text, "lxml")

        blocks = soup.find_all("div", class_='vacancy-info--ieHKDTkezpEj0Gsx')

        for block in blocks:
            block_header = block.find("h2", class_='bloko-header-section-2')
            cur_job = block_header.find("span", class_='magritte-text___tkzIl_6-0-2')

            block_info = block.find("div", class_='info-section--YaC_npvTFcwpFd1I')
            block_city_arr = block_info.find_all("div", class_='narrow-container--HaV4hduxPuElpx0V')
            block_city = block_city_arr[-1]

            cur_city = block_city.find("span", class_='magritte-text___pbpft_4-1-0 magritte-text_style-primary___AQ7MW_4-1-0 magritte-text_typography-label-3-regular___Nhtlp_4-1-0')
            if not desired_city.lower() in cur_city.text.lower():
                continue

            cur_link = block.find("a")
            res.append(f'{translate(cur_job.text, 'ru', cur_language)} - {cur_link['href']}')

    return res