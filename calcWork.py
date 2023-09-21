from loguru import logger
logger.add('log.log')
import requests

def a():
    cookies = {
        'COMPASS': 'apps-spreadsheets=CmUACWuJV9_oaERUVFZ-zvlyj1Dnmfaecha126bXRpZX2iUDA23UIsg3JiFkArE53a5wqilVvm1m_H0eZ-cX1h00_9Zf6x2YG6Wt8t7pEDdhVY9lTGUD5qkgOzAy-hoW3kWPWgeo5hCohrKoBhpnAAlriVcL6QNsy-3R8sFB9shdH2--aIYMNxlTmofkaCZkGzBVdadaOvYD_DKvKBGxcayQ1X-J7VhSEWtsYRs3JRVSKK5jg3Hgw5VdSUgOpj3OP0xATJ0DiYTjYVx9AcdptHIibCMSHA==',
        'SIDCC': 'APoG2W9SgbwRAaXgqwbcctIv5LDdGnyWvOizQluQsefgHtAQogfjehUcMXtAsuoMbRbAMRbxw169',
        '__Secure-1PSIDCC': 'APoG2W_nJBfcw4v-JaOZlhi9E5uLJ_rly6z7iSlCBsTGCNT_xIJ0LrS2d9muULSMHP989d6NZU9M',
        '__Secure-3PSIDCC': 'APoG2W9YybGe0TWxYu77gqVjq7jWKxJwxs2R0wgQkg88ccojEUtBtq6cpUs4ewhf43t1QwICJ9Pq',
        '1P_JAR': '2023-09-21-16',
        'NID': '511=jd52EMqqlAkmmZ_MjvIdYqEYiNUf5CQJa8bmVAccBr6FlSDI_5rHirH1tfV3Mx7QM8Pk18vXr2-PKpdvlIEBos2eyDfSpOTa1KgjFi2gHqIVuzVohxkNJLOKq3VykucI8nhZVNcO5tdoB4PhPrVf-ydKXaFwEPWRVWF1HBJxcDsfU46qv9OMQmNm8Wg41-YEaSgHissbWSU67UaV-z1vc0s4D27bBDb6DHiDjgxYTDUJKl6DfoV6rsBm0drzmRJrktwf5oFJ6m_UG2HuFjaj_Hnz4D6coJCE9Cm1GDlBgG-Hxaga3KroxLGDyiBwHteSUbkAUHd8wLR1TWwMyRYT1TxKAKp3o4OxUs-7QvQ0ycmj3lXvdFPqqx91wQ3oHbRlRhRerKsJb0IYfBhAlaCHdwGZrtUgpaEhHm3DJX93iqLEwx8HzoXNnbEvedtzn8DPGI2ljC6NO66FppUI7IqRlHnE5F5jlk2Wn_PFWOJcx0tU',
        'AEC': 'Ad49MVEop7wdGyitzZWrVkcIM7nuGj9PRX8xlLbFmFIp7ucAeGOYrS804g',
        'APISID': 'OE7LuulmZdm40iQc/A_GNcN_3XZNSAvtQJ',
        'HSID': 'Amnrl22TOylwDcLyB',
        'SAPISID': 'T1Od-XOgS94hKrMO/A6eaL6LYwpA4tOWzT',
        'SID': 'bAiXF4Iq6zkhGuft6O9EkPsNuXSzSU5fJbdYCNIV1C6BL_CWHrdSqK5rW7XcZzHDyAojEg.',
        'SSID': 'AZ_9lljJQ8fJZ7mHe',
        '__Secure-1PAPISID': 'T1Od-XOgS94hKrMO/A6eaL6LYwpA4tOWzT',
        '__Secure-1PSID': 'bAiXF4Iq6zkhGuft6O9EkPsNuXSzSU5fJbdYCNIV1C6BL_CWilTDg2xFEndCvcJyJlMwSg.',
        '__Secure-3PAPISID': 'T1Od-XOgS94hKrMO/A6eaL6LYwpA4tOWzT',
        '__Secure-3PSID': 'bAiXF4Iq6zkhGuft6O9EkPsNuXSzSU5fJbdYCNIV1C6BL_CWtHI_EnLkWSt5YgYUyx8W6w.',
        'S': 'cloudsearch=alnU4tJ-u7q7vLN4iu9ZXCnDCTgjInfnpDePBG0lV5Q',
        'OSID': 'bAiXF-il2h2-4pYwva-KNcxSUt65NZg4TGYoeBHE3Gf639EK6nBmaSb49GsfnGRi_RE4rQ.',
        '__Secure-OSID': 'bAiXF-il2h2-4pYwva-KNcxSUt65NZg4TGYoeBHE3Gf639EKWuUUPIqa5kEq7pxqUxIiXw.',
        'OTZ': '7206621_44_44_123780_40_436260',
        'SEARCH_SAMESITE': 'CgQI0ZgB',
        'ANID': 'AHWqTUmHB9_NTlnhRUp-8cMnIwtZyh1SAd7gFG9XhFxQk7ulDWtvPlRBwdWwGxo5',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Sec-Fetch-Site': 'same-origin',
        # 'Cookie': 'COMPASS=apps-spreadsheets=CmUACWuJV9_oaERUVFZ-zvlyj1Dnmfaecha126bXRpZX2iUDA23UIsg3JiFkArE53a5wqilVvm1m_H0eZ-cX1h00_9Zf6x2YG6Wt8t7pEDdhVY9lTGUD5qkgOzAy-hoW3kWPWgeo5hCohrKoBhpnAAlriVcL6QNsy-3R8sFB9shdH2--aIYMNxlTmofkaCZkGzBVdadaOvYD_DKvKBGxcayQ1X-J7VhSEWtsYRs3JRVSKK5jg3Hgw5VdSUgOpj3OP0xATJ0DiYTjYVx9AcdptHIibCMSHA==; SIDCC=APoG2W9SgbwRAaXgqwbcctIv5LDdGnyWvOizQluQsefgHtAQogfjehUcMXtAsuoMbRbAMRbxw169; __Secure-1PSIDCC=APoG2W_nJBfcw4v-JaOZlhi9E5uLJ_rly6z7iSlCBsTGCNT_xIJ0LrS2d9muULSMHP989d6NZU9M; __Secure-3PSIDCC=APoG2W9YybGe0TWxYu77gqVjq7jWKxJwxs2R0wgQkg88ccojEUtBtq6cpUs4ewhf43t1QwICJ9Pq; 1P_JAR=2023-09-21-16; NID=511=jd52EMqqlAkmmZ_MjvIdYqEYiNUf5CQJa8bmVAccBr6FlSDI_5rHirH1tfV3Mx7QM8Pk18vXr2-PKpdvlIEBos2eyDfSpOTa1KgjFi2gHqIVuzVohxkNJLOKq3VykucI8nhZVNcO5tdoB4PhPrVf-ydKXaFwEPWRVWF1HBJxcDsfU46qv9OMQmNm8Wg41-YEaSgHissbWSU67UaV-z1vc0s4D27bBDb6DHiDjgxYTDUJKl6DfoV6rsBm0drzmRJrktwf5oFJ6m_UG2HuFjaj_Hnz4D6coJCE9Cm1GDlBgG-Hxaga3KroxLGDyiBwHteSUbkAUHd8wLR1TWwMyRYT1TxKAKp3o4OxUs-7QvQ0ycmj3lXvdFPqqx91wQ3oHbRlRhRerKsJb0IYfBhAlaCHdwGZrtUgpaEhHm3DJX93iqLEwx8HzoXNnbEvedtzn8DPGI2ljC6NO66FppUI7IqRlHnE5F5jlk2Wn_PFWOJcx0tU; AEC=Ad49MVEop7wdGyitzZWrVkcIM7nuGj9PRX8xlLbFmFIp7ucAeGOYrS804g; APISID=OE7LuulmZdm40iQc/A_GNcN_3XZNSAvtQJ; HSID=Amnrl22TOylwDcLyB; SAPISID=T1Od-XOgS94hKrMO/A6eaL6LYwpA4tOWzT; SID=bAiXF4Iq6zkhGuft6O9EkPsNuXSzSU5fJbdYCNIV1C6BL_CWHrdSqK5rW7XcZzHDyAojEg.; SSID=AZ_9lljJQ8fJZ7mHe; __Secure-1PAPISID=T1Od-XOgS94hKrMO/A6eaL6LYwpA4tOWzT; __Secure-1PSID=bAiXF4Iq6zkhGuft6O9EkPsNuXSzSU5fJbdYCNIV1C6BL_CWilTDg2xFEndCvcJyJlMwSg.; __Secure-3PAPISID=T1Od-XOgS94hKrMO/A6eaL6LYwpA4tOWzT; __Secure-3PSID=bAiXF4Iq6zkhGuft6O9EkPsNuXSzSU5fJbdYCNIV1C6BL_CWtHI_EnLkWSt5YgYUyx8W6w.; S=cloudsearch=alnU4tJ-u7q7vLN4iu9ZXCnDCTgjInfnpDePBG0lV5Q; OSID=bAiXF-il2h2-4pYwva-KNcxSUt65NZg4TGYoeBHE3Gf639EK6nBmaSb49GsfnGRi_RE4rQ.; __Secure-OSID=bAiXF-il2h2-4pYwva-KNcxSUt65NZg4TGYoeBHE3Gf639EKWuUUPIqa5kEq7pxqUxIiXw.; OTZ=7206621_44_44_123780_40_436260; SEARCH_SAMESITE=CgQI0ZgB; ANID=AHWqTUmHB9_NTlnhRUp-8cMnIwtZyh1SAd7gFG9XhFxQk7ulDWtvPlRBwdWwGxo5',
        'Sec-Fetch-Dest': 'document',
        'Accept-Language': 'ru',
        'Sec-Fetch-Mode': 'navigate',
        'Host': 'docs.google.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15',
        'Referer': 'https://docs.google.com/',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }

    response = requests.get(
        'https://docs.google.com/spreadsheets/d/1v-kbyDHMzfbFQ_WYHLgCb3R5SO7Py_1aBW5kmZm2i8k/edit#gid=1280973776',
        cookies=cookies,
        headers=headers,
    )
    print(response.text)
    with open('file.html', 'w') as file:
    # Записать текст в файл
        # file.write('<meta charset="utf-8">'+response.text)
        file.write(response.text)

def create_pdf():
    a()
    path = '/Users/igorgerasimov/Python/Bitrix/profZaboryGPT/file3.pdf'
    import pdfkit
    # pdfkit.from_url('https://docs.google.com/spreadsheets/d/1v-kbyDHMzfbFQ_WYHLgCb3R5SO7Py_1aBW5kmZm2i8k/edit#gid=1280973776',path)
    pdfkit.from_file('file.html', path,)
    return path
create_pdf()