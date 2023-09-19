from loguru import logger
logger.add('log.log')
import requests

def a():
    cookies = {
    '_ga_SHGXX2LVK3': 'GS1.2.1695040111.1.1.1695040621.60.0.0',
    '_gat_UA-53565554-1': '1',
    '_ga_F2GBR0P5T7': 'GS1.1.1695040110.1.1.1695040593.20.0.0',
    'tmr_detect': '0%7C1695040587942',
    '___dc': 'b239d755-4905-4f00-90da-04961708f378',
    '_ga': 'GA1.1.1105950712.1695040110',
    '_gid': 'GA1.2.635445856.1695040111',
    '_ym_visorc': 'w',
    'mgo_sb_current': 'typ%253Dtypein%257C%252A%257Csrc%253D%2528direct%2529%257C%252A%257Cmdm%253D%2528none%2529%257C%252A%257Ccmp%253D%2528none%2529%257C%252A%257Ccnt%253D%2528none%2529%257C%252A%257Ctrm%253D%2528none%2529%257C%252A%257Cmango%253D%2528none%2529',
    'mgo_sb_session': 'pgs%253D5%257C%252A%257Ccpg%253Dhttps%253A%252F%252Fwww.masterovit.ru%252Fraschet-zabora-iz-profnastila%252F',
    'mgo_sid': '8544s16ln8110025gjbo',
    '_ymab_param': 'PwYA17oPsJ9Yaus-LfeEve9Iq_WHbxWy2JfKQed3MqHObBtZh9bIzrzqvxzihN5J_QNnAG9q8CjE2VDTXXAMIe3vkiE',
    'cityDisplayID': '-1',
    'tmr_lvid': 'cecc2fc3c515b597f78777b6b8f2f994',
    'tmr_lvidTS': '1695040109440',
    'roistat_call_tracking': '1',
    'roistat_cookies_to_resave': 'roistat_visit%2Croistat_first_visit%2Croistat_visit_cookie_expire%2Croistat_is_need_listen_requests%2Croistat_is_save_data_in_cookie%2Croistat_ab%2Croistat_ab_submit%2Croistat_call_tracking%2Croistat_emailtracking_email%2Croistat_emailtracking_tracking_email%2Croistat_emailtracking_emails',
    'roistat_emailtracking_email': 'null',
    'roistat_emailtracking_emails': '%5B%5D',
    'roistat_emailtracking_tracking_email': 'null',
    'mgo_cnt': '2',
    '_ym_isad': '1',
    'mgo_sb_first': 'typ%253Dtypein%257C%252A%257Csrc%253D%2528direct%2529%257C%252A%257Cmdm%253D%2528none%2529%257C%252A%257Ccmp%253D%2528none%2529%257C%252A%257Ccnt%253D%2528none%2529%257C%252A%257Ctrm%253D%2528none%2529%257C%252A%257Cmango%253D%2528none%2529',
    'mgo_sb_migrations': '1418474375998%253D1',
    'mgo_uid': 'PzZTnMzOjgzI3VEyc2iR',
    'BX_USER_ID': '11cfa6453fa55602de532c8bc540b477',
    'roistat_first_visit': '11457612',
    'roistat_is_need_listen_requests': '0',
    'roistat_is_save_data_in_cookie': '1',
    'roistat_visit': '11457612',
    'roistat_visit_cookie_expire': '1209600',
    '_ym_d': '1695040110',
    '_ym_uid': '169504011031833922',
    'PHPSESSID': '3ZIGkrCZXY7uWlQaLSK2ZT0mj7NUAO0m',
    '__ddg1_': 'PfG3Xqysu8eVreOcjbHM',
}

    headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': 'text/html, */*; q=0.01',
    'Sec-Fetch-Site': 'same-origin',
    'Accept-Language': 'ru',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Sec-Fetch-Mode': 'cors',
    'Host': 'www.masterovit.ru',
    'Origin': 'https://www.masterovit.ru',
    # 'Content-Length': '184',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15',
    'Referer': 'https://www.masterovit.ru/raschet-zabora-iz-profnastila/',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    # 'Cookie': '_ga_SHGXX2LVK3=GS1.2.1695040111.1.1.1695040621.60.0.0; _gat_UA-53565554-1=1; _ga_F2GBR0P5T7=GS1.1.1695040110.1.1.1695040593.20.0.0; tmr_detect=0%7C1695040587942; ___dc=b239d755-4905-4f00-90da-04961708f378; _ga=GA1.1.1105950712.1695040110; _gid=GA1.2.635445856.1695040111; _ym_visorc=w; mgo_sb_current=typ%253Dtypein%257C%252A%257Csrc%253D%2528direct%2529%257C%252A%257Cmdm%253D%2528none%2529%257C%252A%257Ccmp%253D%2528none%2529%257C%252A%257Ccnt%253D%2528none%2529%257C%252A%257Ctrm%253D%2528none%2529%257C%252A%257Cmango%253D%2528none%2529; mgo_sb_session=pgs%253D5%257C%252A%257Ccpg%253Dhttps%253A%252F%252Fwww.masterovit.ru%252Fraschet-zabora-iz-profnastila%252F; mgo_sid=8544s16ln8110025gjbo; _ymab_param=PwYA17oPsJ9Yaus-LfeEve9Iq_WHbxWy2JfKQed3MqHObBtZh9bIzrzqvxzihN5J_QNnAG9q8CjE2VDTXXAMIe3vkiE; cityDisplayID=-1; tmr_lvid=cecc2fc3c515b597f78777b6b8f2f994; tmr_lvidTS=1695040109440; roistat_call_tracking=1; roistat_cookies_to_resave=roistat_visit%2Croistat_first_visit%2Croistat_visit_cookie_expire%2Croistat_is_need_listen_requests%2Croistat_is_save_data_in_cookie%2Croistat_ab%2Croistat_ab_submit%2Croistat_call_tracking%2Croistat_emailtracking_email%2Croistat_emailtracking_tracking_email%2Croistat_emailtracking_emails; roistat_emailtracking_email=null; roistat_emailtracking_emails=%5B%5D; roistat_emailtracking_tracking_email=null; mgo_cnt=2; _ym_isad=1; mgo_sb_first=typ%253Dtypein%257C%252A%257Csrc%253D%2528direct%2529%257C%252A%257Cmdm%253D%2528none%2529%257C%252A%257Ccmp%253D%2528none%2529%257C%252A%257Ccnt%253D%2528none%2529%257C%252A%257Ctrm%253D%2528none%2529%257C%252A%257Cmango%253D%2528none%2529; mgo_sb_migrations=1418474375998%253D1; mgo_uid=PzZTnMzOjgzI3VEyc2iR; BX_USER_ID=11cfa6453fa55602de532c8bc540b477; roistat_first_visit=11457612; roistat_is_need_listen_requests=0; roistat_is_save_data_in_cookie=1; roistat_visit=11457612; roistat_visit_cookie_expire=1209600; _ym_d=1695040110; _ym_uid=169504011031833922; PHPSESSID=3ZIGkrCZXY7uWlQaLSK2ZT0mj7NUAO0m; __ddg1_=PfG3Xqysu8eVreOcjbHM',
    'X-Requested-With': 'XMLHttpRequest',
}

    data = {
        'proflistget': '',
        'calc_type': 'calc_type',
        'dlina': '12',
        'visota': '10.8',
        'ral': '0',
        'mobile_depth': '0',
        'mobile_cover': '0',
        'width_stolb': '1.5',
        'ryad': '3',
        'okras': '0',
        'kolvo_vorota': '3',
        'vshir': '3.0',
        'kolvo_kalitka': '2',
        'km': '123',
        'city': '181',
}

    response = requests.post('https://www.masterovit.ru/calculator/proflist/ajax.php', cookies=cookies, headers=headers, data=data)
    #file = open('file.txt', 'w')
    with open('file.html', 'w') as file:
    # Записать текст в файл
        file.write('<meta charset="utf-8">'+response.text)

def create_pdf():
    a()
    path = '/Users/igorgerasimov/Python/Bitrix/profZaboryGPT/file.pdf'
    import pdfkit
    pdfkit.from_file('file.html', path,)
    return path