import requests
from xml.etree import ElementTree


def update_data_library():
    url = 'http://api.data.go.kr/openapi/tn_pubr_public_lbrry_api'
    params = {'serviceKey': 'Sqf+Tjc3JdQg5Q27NrXVwov2IdeC3sM4kwf9IIAy3CK2rN8682lvulwQI48i7nZV7ReVX3S/8vjbZdkj+Q5NAg==', 'ctprvnNm': '서울특별시'}

    response = requests.get(url, params=params)

    root_element = ElementTree.fromstring(response.content)
    librarys = []
    iter_element = root_element.iter(tag="item")
    for element in iter_element:
        library = {}
        if element.find("homepageUrl").text != "":
            library['lbrryNm'] = element.find("lbrryNm").text
            library['ctprvnNm'] = element.find("ctprvnNm").text
            library['signguNm'] = element.find("signguNm").text
            library['rdnmadr'] = element.find("rdnmadr").text
            library['homepageUrl'] = element.find("homepageUrl").text
            library['phoneNumber'] = element.find("phoneNumber").text

        librarys.append(library)
    return librarys
