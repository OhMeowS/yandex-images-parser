import requests
from bs4 import BeautifulSoup
import json
import os

def get_data():

    cookies = {
        'is_gdpr': '0',
        'is_gdpr_b': 'CMyzPRD7lQEoAg==',
        '_yasc': 'Wv2gjUYC7QuSbub+bfEHY6Piq0V+KElZM/j+hukAuexwepTz26hWRE5vT+nx5UnrjCGhy+mGhhzD',
        'i': 'i6xpXgPVEWHD+bsOQag9ZXkTAwTynbd4XisyWMjhEOHdN0+l+ndYdbaLhQ7G/YlARsCnH9lhGf7jn7pMEtNpkw9QFfg=',
        'ys': 'wprid.1668741700119044-17610774625560014796-vla1-3235-vla-l7-balancer-8080-BAL-2753#c_chck.910925448',
        'yandexuid': '7174662161668701910',
        'yp': '1700237925.p_sw.1668701925#1669306727.mcv.0#1669306727.mcl.#1669306728.szm.1_25:1536x864:1536x408#1668824978.ln_tp.true',
        'yabs-frequency': '/5/0000000000000000/swvnE0daUaPyIQT-MMkamxpYKNn99m00/',
        'yuidss': '7174662161668701910',
        'ymex': '1984061927.yrts.1668701927',
        'gdpr': '0',
        '_ym_uid': '1668701926992279169',
        '_ym_d': '1668701927',
        '_ym_isad': '2',
        'cycada': 'ORnhAfdS638o+C4RgoCtKztWfUxb3mUkYp6zEriZMbU=',
        'spravka': 'dD0xNjY4NzcwNTI5O2k9MTg4LjE2Mi4yMjkuMTUyO0Q9NjI1ODJGREYzNDNBRDlFMTI1RTZFMTdDMTc2QjQ1MEZFRTc1NUE0M0ZFRkRBMDFGMEE5QTY4MEI4NUE5RTQyQjE5QzNCRTg1O3U9MTY2ODc3MDUyOTUyNDA3NDc5MTtoPTJkM2MxYTM4ZjYzMWRiMjJmNDMyZTUxZDEwNzI0ODM2',
        '_ym_visorc': 'b',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': 'https://yandex.ru/showcaptcha?mt=068DBD0BC1AC298E1D20BA4077E3E32DAF2ABC6178A310CE18242787DEA7C838&retpath=aHR0cHM6Ly95YW5kZXgucnUvaW1hZ2VzL3NlYXJjaD90ZXh0PSVEMCVCNSVEMCVCRCVEMCVCRSVEMSU4MiZmcm9tPXRhYmJhciZwPTEmbHI9NzU%2C_7774ff8c1857375cd803dd4aafbbac8c&t=3/1668770513/debe1e04e964cd4fe998160cfb18aecf&u=1a150b5e-718ffbc0-a7bef71c-f0f8a626&s=bc51c20c26c56df79ba98811a7fa9391',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
    }
    w = 0 # задаваемый параметр по ширене
    h = 0 # задаваемый параметр по высоте
    quantity_scriping = 2000 #Количество фотографий, которые нужно собрать
    word_for_find = []
    words = ['фото']
    for item in words:
        item = item.strip().replace(' ','+')
        word_for_find.append(item)

        
    for word in word_for_find:
        try:
            os.mkdir(word.replace('+',' '))
        except:
            pass
        schet = 0
        for j in range(0, 999):
            url = f'https://yandex.ru/images/search?text={word}&from=tabbar&p={j}&lr=75'
            response = requests.get(url=url, headers=headers, cookies=cookies)
            soup = BeautifulSoup(response.text, 'lxml')
            serp_list = soup.find('div', class_='SerpList')
            try:
                serp_items = serp_list.find_all('div', class_= 'SerpItem')
            except AttributeError:
                print(f'------------Картинки на слово {word} закончились-------------')
                schet = quantity_scriping
                break 

            for i in serp_items:
                dict_photo_url = {}
                json_html = json.loads(i.get("data-bem"))
                img_url = json_html['SerpItem']['href']
                img_url_params = json_html['SerpItem']['dups']
                schet += 1
                for dup in range(len(img_url_params)):
                    try:
                        key_h = img_url_params[dup]['origin']['h']
                        key_w = img_url_params[dup]['origin']['w']
                        value = img_url_params[dup]['origin']['url']
                    except:
                        key_w = img_url_params[dup]['w']
                        key_h = img_url_params[dup]['h']
                        value = img_url_params[dup]['url']
                    key, val = value, [key_w, key_h]
                    dict_photo_url[key] = val
                result = {}
                for key in dict_photo_url:
                    val = abs(w-int(dict_photo_url[key][0]))+abs(h-int(dict_photo_url[key][1]))
                    result[key] = val

                back = None
                url = ''
                for key in result:
                    if back == None:
                        back = result[key]
                        continue
                    if back > result[key]:
                        back = result[key]
                        url = key
                print(f'[INFO]Cпаршено {schet} из {quantity_scriping} картинок в папку {word}')
                try:

                    response = requests.get(url=img_url)
                    img_option = open(f'{word.replace("+"," ")}/{schet}_big.jpg', 'wb')
                    img_option.write(response.content)
                    img_option.close()

                    small = 'https:' + json_html['SerpItem']['thumb']['url']
                    response = requests.get(url=small)
                    img_option = open(f'{word.replace("+"," ")}/{schet}_small.jpg', 'wb')
                    img_option.write(response.content)
                    img_option.close()

                    try:
                        response = requests.get(url=url)
                        img_option = open(f'{word.replace("+"," ")}/{schet}_по_настройкам.jpg', 'wb')
                        img_option.write(response.content)
                        img_option.close()
                    except:
                        pass
                except:
                    print('Disconnect')
                    schet -= 1
                if schet == quantity_scriping:
                    break
            if schet == quantity_scriping:
                break
    print("--------КОНЕЦ-------------")


def main():
    get_data()


if __name__ == '__main__':
    main()
