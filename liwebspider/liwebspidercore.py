#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import logging

from bs4 import BeautifulSoup

import imgspiderconf as Config

logging.basicConfig(format='%(asctime)s %(levelname)8s %(message)s',
                    filename=LOG_FILE, filemode='w')
logger = logging.getLogger().setLevel(logging.DEBUG)


class Spider(object):

    def __init__(self):
        self.Config = Config

    def GrabHtmlContent(self, url):
        if not url:
            logger.warning('grab html content failed: no url provided.')
            return None

        request_counter = [0]

        def _request_content(user_agent='Chrome'):
            if request_counter[0] > self.Config.GrabHtmlContent['MaxTryCount']:
                return None

            request_counter[0] += 1

            try:
                req = urllib2.Request(url, headers={'User-Agent': user_agent})
                con = urllib2.urlopen(req)
                return con
            except Exception as e:
                # if forbidden, try it [GrabHtmlContent_MaxTryCount] more times
                # TO BE CLEAR : what the hell 'user_agent' is for ?
                return _request_content(random.sample('abcdefghijklmnopqrstuvwxyz', 10))

        con = request_content()

        if con.code != 200:
            msg = 'grab html content failed: http code returns abnormally'
            logger.warning(msg)
            raise Exception('msg')

        return con.read()

    def ContentParser(self, html_content):
        HitTemplate = self.Config.HitTemplate['Element']


def extract_elem_from_raw_tag(tag_row, tag_text, resize_image=False):
    print "into func ing.."
    # find author and id first, as the rss title
    author_tag = tag_row.find(name='div', class_='author')
    author = author_tag.find(name='strong').string
    logging.debug('author = %s', author)

    id_tag = tag_text.find(name='span', class_='righttext')
    id = id_tag.string
    logging.debug('id = %s', id)

    # then find the img link
    orig_img_tag = tag_text.find(name='a', class_='view_img_link')
    orig_img_link = orig_img_tag.get('href')
    logging.debug('orig_img_link = %s', orig_img_link)

    # and at last get tht real image content
    img_tag = tag_text.find(name='img')
    img_link = img_tag.get('src')
    logging.debug('img_link = %s', img_link)

    image_con = grab_html_content(img_link)

    if resize_image:
        # resize the image using pillow
        im = Image.open(cStringIO.StringIO(image_con))
        new_size = (int(im.size[0] / IMG_SIZE_RATIO), int(im.size[1] / IMG_SIZE_RATIO))
        im.resize(new_size)

        image_io = cStringIO.StringIO()
        im.save(image_io, im.format)
        image_con = image_io.getvalue()
        image_io.close()

    return {'id': id,
            'author': author,
            'link': img_link,
            'content': image_con}


def extract_elem_from_raw_tag_entry(tag_row, tag_text, resize_image=False):
    global _MyThreadDigger
    _MyThreadDigger.AddTask(extract_elem_from_raw_tag, tag_row, tag_text, resize_image)


def filter_html_content(html_content, recursive=False):
    if not html_content:
        logger.warning('filter html content failed : no html content provided.')
        return None

    soup = BeautifulSoup(html_content, "html.parser")

    if __debug__:
        with open(Debug_FilterHtmlContent_LocalFileName, "w") as f:
            f.write(soup.prettify().encode('utf-8'))

    raw_tags_row = soup.find_all(name='div', class_='row')
    raw_tags_text = soup.find_all(name='div', class_='text')
    # elems = []

    print "size of raw_tags_row= %d" % len(raw_tags_row)
    print "size of raw_tags_text= %d" % len(raw_tags_text)
    for tag_row, tag_text in itertools.izip(raw_tags_row, raw_tags_text):
        elem = extract_elem_from_raw_tag_entry(tag_row, tag_text)
    # elems.append(elem)

    if recursive is True:
        cp_pagenavi_tag = soup.body.find(name='div', class_='cp-pagenavi')

        def page_filter(tag):
            return tag.has_attr('href') and not tag.has_attr('class')

        rest_two_pages = cp_pagenavi_tag.find_all(page_filter)

        for page in rest_two_pages:
            previous_url = page.get('href')

            logging.debug('previous_url = %s', previous_url)

            previous_html = grab_html_content(previous_url)
            filter_html_content(previous_html, False)
            # elems.extend(previous_elems)

    # elems.reverse()
    # return elems


def filter_html_content_entry(html_content):
    global _MyThreadDigger
    _MyThreadDigger = ThreadDigger(DIGGER_THREAD_COUNT)

    filter_html_content(html_content, True)

    _MyThreadDigger.StartToDig()

    elems = _MyThreadDigger.WaitToEnd()

    return elems
