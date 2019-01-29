import sys
import os
import requests
import argparse
import json
import mongoengine
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from multiprocessing.dummy import Pool as ThreadPool
import artwork

RECONNECT_TIME = 50


def get_html(url, params="", headers="", counter=0):
    try:
        resp = requests.get(url, params=params, headers=headers)
    except requests.exceptions.ConnectionError as e:
        if counter < RECONNECT_TIME:
            return get_html(url, counter=counter + 1)
        else:
            print(e, "<", url, ">")
            return ""
    except requests.exceptions.ConnectTimeout as e:
        if counter < RECONNECT_TIME:
            return get_html(url, counter=counter + 1)
        else:
            print(e, "<", url, ">")
    else:
        return resp.text


def url_generator(url, datatype=""):
    parsed_url = urlparse(url)
    url_base = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_url)
    html = get_html(url)[3:]
    soup = BeautifulSoup(html, 'html.parser')
    count = soup.find("span", {'class': 'count'}).text
    count = int(count)
    if count > 10000:
        tags = soup.find_all("a", {'data-type': datatype})
        for tag in tags:
            sub_url = url_base + tag['href']
            for r in url_generator(sub_url, 'techniques'):
                yield r
    else:
        for i in range(0, int(count/20) + 1):
            useful_url = url + '&ajax=1&page=' + str(i)
            yield useful_url


def louvre_miner(url):
    print(url)
    html = get_html(url)[3:]
    soup = BeautifulSoup(html, 'html.parser')
    imgs = soup.find_all("img")
    parsed_url = urlparse(url)
    url_base = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_url)
    if not imgs:
        return
    for img in imgs:
        info_field = img.parent
        info_url = url_base + info_field['href']
        img_url = img['src']
        try:
            art = info_miner(info_url)
        except:
            continue
        art.origin_img = img_url
        art.description = description_miner(art.title)
        art.training_img = training_img_miner(art.title)
        try:
            art.save()
        except mongoengine.errors.NotUniqueError as e:
            print(e)


def info_miner(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    parsed_url = urlparse(url)
    url_base = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_url)
    title = soup.find_all('h1')[1].text
    author_dates = soup.find('span', {'class': 'dates'})
    if author_dates:
        author_info = author_dates.parent
        author_dates = author_dates.text
        author_name = author_info.a.text
        author_link = url_base + author_info.a['href']
        author = artwork.Author(author_name, author_dates, author_link)
        art = artwork.Artwork(title=title, author=author)
    else:
        art = artwork.Artwork(title, None)
    try:
        images_field = soup.find('h2', text='Detail image(s)').parent
    except AttributeError:
        return art
    images = images_field.find_all('img')
    for image in images:
        img = artwork.Image(img_url=image['src'])
        art.detail_img.append(img)
    return art


def description_miner(title):
    search_item = title.replace(" ", "+")
    search_item = title
    url = "http://www.google.co.in/search"
    params = {"source": "hp", "q": search_item + "+louvre", "oq": search_item + "+louvre",
              "gs_l": "psy-ab.12...10773.10773.0.22438.3.2.0.0.0.0.135.221.1j1.2.0..."
                      ".0...1.2.64.psy-ab..1.1.135.6..35i39k1.zWoG6dpBC3U",
              'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
                            "(KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
              }
    html = get_html(url, params=params)
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all('h3', attrs={'class': 'r'})
    for link in links:
        try:
            link_href = link.a['href']
        except:
            print(sys.exc_info()[0])
            continue
        if "www.louvre.fr" in link_href:
            louvre_url = link_href.split("=", 1)[1]
            louvre_html = get_html(louvre_url)
            louvre_soup = BeautifulSoup(louvre_html, "html.parser")
            louvre_description = louvre_soup.find("div", attrs={'class': 'col-desc'})
            return str(louvre_description)
        else:
            return "None"


def training_img_miner(title):
    url = "https://www.google.co.in/search?q="+title.replace(" ", "+")+"&source=lnms&tbm=isch"
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
        }
    imgs = []
    html = get_html(url, headers=header)
    soup = BeautifulSoup(html, "html.parser")
    img_fields = soup.find_all("div", {"class": "rg_meta"})
    for img_field in img_fields:
        img_json = json.loads(img_field.text)
        img_url = img_json['ou']
        img = artwork.Image(img_url=img_url)
        imgs.append(img)
    return imgs


def clear_database():
    artworks = artwork.Artwork.objects
    for art in artworks:
        art.delete()


def download_img(img_dir, url):
    abs_dir = os.path.dirname(os.path.realpath(__file__))
    img_name = url.split('/')[-1]
    img_req = requests.get(url)
    if img_req.status_code == 200:
        with open(img_dir + '/' + img_name, 'wb') as f:
            f.write(img_req.content)
    img_path = '/'.join([abs_dir, img_dir, img_name])
    return img_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-C', '--clear', action='store_true', help='Clear the database')
    ap.add_argument('-g', '--generate', action='store_true', help='Get data from websites and put it into database')
    ap.add_argument('-d', '--description', action='store_true'
                    , help='Get description data from websites and put it into database')
    ap.add_argument('-i', '--image', action='store_true', help='Get more images from google and put it into database')
    ap.add_argument('-D', '--download', action='store_true'
                    , help='download images from website and put it into local storage')
    args = ap.parse_args()

    if args.clear:
        clear_database()

    if args.generate:
        url = "http://art.rmngp.fr/en/library/artworks?locations=mus%C3%A9e%20du%20Louvre"
        urls = []
        for useful_url in url_generator(url, 'periods'):
            urls.append(useful_url)
        pool = ThreadPool(4)
        pool.map(louvre_miner, urls)
        pool.close()
        pool.join()

    if args.description:
        for art in artwork.Artwork.objects:
            if not art.description:
                description = description_miner(art.title)
                try:
                    art.update(**{'description': description})
                except:
                    print(sys.exc_info()[0])
    if args.image:
        for art in artwork.Artwork.objects:
            if len(art.training_img) == 0:
                imgs = training_img_miner(art.title)
                try:
                    art.update(**{'training_img': imgs})
                except:
                    print(sys.exc_info()[0])
    if args.download:
        if not os.path.exists("imgs"):
            os.makedirs("imgs")
        for art in artwork.Artwork.objects:
            img_dir = "imgs/" + str(art.id)
            if not os.path.exists(img_dir):
                os.makedirs(img_dir)
            origin_img_path = download_img(img_dir, art.origin_img)
            detail_imgs = []
            training_imgs = []
            for img in art.detail_img:
                url = img.img_url
                detail_img_path = download_img(img_dir, url)
                detail_imgs.append(artwork.Image(img_url=url, img_path=detail_img_path))
            for img in art.training_img:
                url = img.img_url
                train_img_path = download_img(img_dir, url)
                training_imgs.append(artwork.Image(img_url=url, img_path=train_img_path))
            art.update(**{'origin_img_path': origin_img_path,
                          'detail_img': detail_imgs, 'training_img': training_imgs})
            break


if __name__ == "__main__":
    main()
