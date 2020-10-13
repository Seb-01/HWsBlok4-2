from collections import Counter

from django.shortcuts import render_to_response

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    # проверяем параметры, которые пришли вместе с запросом:

    # если параметра from-landing не передано, то вернет None!!!
    landing_name = request.GET.get('from-landing')
    if landing_name == 'original':
        # http://127.0.0.1:8000/?from-landing=original
        counter_click['original'] += 1
    elif landing_name == 'test':
        # http://127.0.0.1:8000/?from-landing=test
        counter_click['test'] += 1
    else :
        counter_click['no_FROM_GET_param'] += 1

    return render_to_response('index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов

    #проверяем параметры, которые пришли вместе с запросом:

    #если параметра ab-test-arg не передано, то вернет None!!!
    landing_name = request.GET.get('ab-test-arg')
    if landing_name == 'original':
        #http://127.0.0.1:8000/landing?ab-test-arg=original
        counter_show['original']+=1
        return render_to_response('landing.html')
    elif landing_name == 'test':
        # http://127.0.0.1:8000/landing?ab-test-arg=test
        counter_show['test'] += 1
        return render_to_response('landing_alternate.html')
    else :
        counter_show['no_AB_GET_param'] += 1
        return render_to_response('no_landing.html')


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:
    # всего кликов
    # оригинал
    if counter_show['original'] == 0:
        original_rate = float(0)
    else:
        original_rate = float(counter_click['original']/counter_show['original'])

    # тест
    if counter_show['test'] == 0:
        test_rate = float(0)
    else:
        test_rate = float(counter_click['test'] / counter_show['test'])

    #приводим к нужному формату

    return render_to_response('stats.html', context={
        'test_conversion': f'{test_rate:.1f}',
        'original_conversion': f'{original_rate:.1f}'
    })
