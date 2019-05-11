import urllib.request
from bs4 import BeautifulSoup


# Получаем исходный код страницы
def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()


# Парсим секреты с одной страницы в список.
def scraping_secrets_from_page(html):
    soup = BeautifulSoup(html)
    secrets = []
    div = soup.find_all('div', class_='shortContent')
    for secret in div:
        secrets.append(secret.text)
    return secrets


# Переходим на следующую страницу.
def paginate(url):
    if ("page" in url):
        cols = url.split('/')
        cols[-1] = str(int(cols[-1]) + 15)
        return "/".join(cols)
    else:
        return url + "/page/15"


# Парсим все секреты из категории в список списков (потому что иногда полезно было бы вытащить секреты с одной страницы, а не со всех разом).
def scraping_all_secrets_from_category(url):
    secrets = []
    while (not "В данную категорию пока не добавлено ни одного секрета." in BeautifulSoup(get_html(url)).text):
        secrets.append(scraping_secrets_from_page(get_html(url)))
        print(len(secrets))
        url = paginate(url)        
    return secrets


# Парсим плохие рассказы.
def scraping_bad_tales(bad_categories):
    secrets = []
    print("Starting scraping1...")
    for category in bad_categories:
        secrets.append(scraping_all_secrets_from_category(category))            
    flatten_secrets = (make_beautiful_list(secrets))
    return flatten_secrets


# Делаем список из списка списков списков (категория-страница-секрет).
def make_beautiful_list(big_list):
    return [item for sublist in [item for sublist in big_list for item in sublist] for item in sublist]


# Парсим ссылки на стихи с детского сайта.
def scraping_links(url):
    soup = BeautifulSoup(get_html(url))
    links = []
    trs = soup.table.find_all('a', href=True)
    for tr in trs:
        links.append(tr['href'])
    return links


# Парсим все стихи от одного автора.
def scraping_all_verse_from_category(url):
    links = scraping_links(url)
    tales = []
    for link in links:
        tales.append(scraping_verse('https://deti-online.com' + link))
    return tales


# Парсим один стих.
def scraping_verse(url):
    soup = BeautifulSoup(get_html(url))
    verse = ""
    tags = soup.find('div', class_='r').find_all('p')

    for tag in tags:
        for string in tag.contents:
            try:
                verse += string + ' '
            except:
                print('ebanyi site')
    return verse


# Парсим стихи из других категорий, тк сайт размечен по-разному.
def scraping_other_verses(url):
    soup = BeautifulSoup(get_html(url))
    divs = soup.find_all('div', class_='txt')
    verses = []
    for verse in divs:
        verse_global = ""
        for tag in verse.contents:
            for string in tag.contents:
                try:
                    verse_global += string + ' '
                except:
                    print('ebaniy site')
        verses.append(verse_global)
    return verses


# Парсим хорошие рассказы.
def scraping_good_tales(good_categories):
    tales = []
    for category in good_categories:
        tales = tales + scraping_all_verse_from_category(category)
    return tales


# Парсим хорошие рассказы (страниы сайта с другой разметкой.)
def scraping_good_other_tales(good_categories):
    tales = []
    for category in good_categories:
        tales = tales + scraping_other_verses(category)
    return tales


def get_bad_categories(a):
    vulgar = 'https://ideer.ru/secrets/vulgar'
    angry = 'https://ideer.ru/secrets/angry'
    pizdec = 'https://ideer.ru/secrets/pizdec'
    lust = 'https://ideer.ru/secrets/lust'
    cherhuha = 'https://ideer.ru/secrets/cherhuha'
    cruelty = 'https://ideer.ru/secrets/cruelty'
    ebanko = 'https://ideer.ru/secrets/ebanko'
    fuuu = 'https://ideer.ru/secrets/fuuu'
    betrayal = 'https://ideer.ru/secrets/betrayal'
    alco = 'https://ideer.ru/secrets/alco'
    boom = 'https://ideer.ru/secrets/boom'
    envy = 'https://ideer.ru/secrets/envy'
    enrage = 'https://ideer.ru/secrets/enrage'

    bad_categories = [vulgar, angry, pizdec, lust, cherhuha, cruelty, ebanko, fuuu, betrayal, alco, boom, envy, enrage]

    return bad_categories


def get_good_categories(a):
    barto = 'https://deti-online.com/stihi/stihi-agnii-barto/'
    zahoder = 'https://deti-online.com/stihi/stihi-zahodera/'
    mihalkov = 'https://deti-online.com/stihi/stihi-mihalkova/'
    berestov = 'https://deti-online.com/stihi/stihi-berestova/'
    sapgir = 'https://deti-online.com/stihi/stihi-sapgira/'
    blaginina = 'https://deti-online.com/stihi/stihi-blaginina/'
    surikov = 'https://deti-online.com/stihi/stihi-surikova/'
    shemyakina = 'https://deti-online.com/stihi/stihi-shemyakina/'
    gusarova = 'https://deti-online.com/stihi/stihi-gusarova/'
    uspenskyi = 'https://deti-online.com/stihi/stihi-uspenskogo/'
    mecgera = 'https://deti-online.com/stihi/stihi-mecgera/'

    good_tales = [barto, zahoder, mihalkov, berestov, sapgir, blaginina, surikov, shemyakina, gusarova, uspenskyi,
                  mecgera]

    return good_tales


def get_good_categories_other():

    animals = 'https://deti-online.com/stihi/stihi-pro-zhivotnyh/'
    birds = 'https://deti-online.com/stihi/stihi-pro-ptic/'
    fishes = 'https://deti-online.com/stihi/stihi-pro-ryb/'
    nasekomye = 'https://deti-online.com/stihi/stihi-pro-nasekomyh/'
    winter = 'https://deti-online.com/stihi/zima/'
    osen = 'https://deti-online.com/stihi/osen/'
    fruits = 'https://deti-online.com/stihi/ovoschi-i-frukty/'
    sea = 'https://deti-online.com/stihi/stihi-pro-more/'
    mushrooms = 'https://deti-online.com/stihi/griby/'
    "help me pls"
    flowers = 'https://deti-online.com/stihi/cvety/'
    spring = 'https://deti-online.com/stihi/vesna/'
    summer = 'https://deti-online.com/stihi/leto/'
    stValentine = 'https://deti-online.com/stihi/stihi-valentina/'
    fevral = 'https://deti-online.com/stihi/stihi-23-fevralya/'
    mart = 'https://deti-online.com/stihi/stihi-8-marta/'
    masl = 'https://deti-online.com/stihi/stihi-maslenica/'
    easter = 'https://deti-online.com/stihi/stihi-pasha/'
    fstsept = 'https://deti-online.com/stihi/stihi-1-sentyabrya/'
    teacher = 'https://deti-online.com/stihi/stihi-den-uchitelya/'
    motherDay = 'https://deti-online.com/stihi/stihi-den-materi/'
    xmas = 'https://deti-online.com/stihi/stihi-rozhdestvo/'
    newyear = 'https://deti-online.com/stihi/stihi-pro-novyy-god/'
    tree = 'https://deti-online.com/stihi/stihi-pro-novogodnyuyu-elku/'
    forlittle = 'https://deti-online.com/stihi/novogodnie-stihi-dlya-malenkih/'
    moroz = 'https://deti-online.com/stihi/stihi-pro-deda-moroza/'
    snegurochka = 'https://deti-online.com/stihi/stihi-pro-snegurochku/'
    sneg = 'https://deti-online.com/stihi/stihi-pro-snezhinki/'
    snowman = 'https://deti-online.com/stihi/stihi-pro-snegovika/'

    good_tales_other = [snowman, sneg, snegurochka, moroz, forlittle, tree, newyear, xmas, motherDay, teacher, fstsept, easter, masl, mart, fevral, stValentine, summer, spring, flowers, mushrooms, sea, fruits, osen, animals, birds, fishes, winter, nasekomye]

    return good_tales_other

