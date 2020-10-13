from django.shortcuts import render_to_response, redirect
from django.urls import reverse
from math import ceil
from urllib.parse import urlencode

from django.conf import settings
# для работы с DictReader
from csv import DictReader

def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):

    # загружаем данные из файла
    data_file_name = settings.BUS_STATION_CSV
    all_rows = []
    part_of_data = []

    # файл в кодировке cp1251!
    with open(data_file_name,encoding='cp1251',newline='') as csvfile:
        bs_data = DictReader(csvfile)

        # сколько всего строк? Так нельзя: потом невозможно будет в in прочитать!
        #number_of_rows=len(list(bs_data))-1
        all_rows = list(bs_data)
        number_of_rows = len(all_rows) - 1
        # кол-во одновременно выводимых строк на странице
        rows_in_page = settings.ROWS_IN_INDEXPAGE
        # всего страниц с округлением в большую сторону
        total_pages = ceil(float(number_of_rows/rows_in_page))


        # номер текущей страницы из параметров запроса
        current_page = int(request.GET.get('page', 1))
        if (current_page == None) or (current_page < 1):
            current_page=1
        elif current_page > total_pages:
            current_page=total_pages

    if current_page ==1:
        current_list = all_rows[1:11]
    else:
        current_list=all_rows[((current_page-1) * rows_in_page -1):(current_page * rows_in_page)]

    # формируем порцию данных для вывода согласно current_page
    for row in current_list:
        page_row=dict()
        page_row['Name']=row['Name']
        page_row['Street'] = row['Street']
        page_row['District'] = row['District']
        part_of_data.append(page_row)


    # формируем prev- и next- URL
    base_URL=reverse('bus_stations')
    if current_page == 1:
        next_page_url = base_URL + '?' + urlencode({'page':2})
        prev_page_url = None
    elif current_page == total_pages:
        next_page_url = None
        prev_page_url = base_URL + '?' + urlencode({'page':total_pages-1})
    else:
        next_page_url = base_URL + '?' + urlencode({'page':current_page + 1})
        prev_page_url = base_URL + '?' + urlencode({'page': current_page - 1})

    return render_to_response('index.html', context={
        #'bus_stations': [{'Name': 'название', 'Street': 'улица', 'District': 'район'}],
        'bus_stations': part_of_data,
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    })

