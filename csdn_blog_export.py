import argparse
import json
import pathlib
import re
import time

import requests

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'


def get_article_list(username):
    url = 'https://blog.csdn.net/community/home-api/v1/get-business-list'
    params = {'page': 1, 'size': 50, 'businessType': 'blog', 'noMore': 'false', 'username': username}
    headers = {'User-Agent': USER_AGENT}
    current_page = 1
    article_list = []
    while True:
        params['page'] = current_page
        response = requests.get(url, params=params, headers=headers)
        if response.status_code != 200:
            print('Failed to get article list at page {}, status code is {}'.format(
                current_page, response.status_code))
            break
        articles = response.json()
        if not articles['data']['list']:
            break
        article_list.extend(articles['data']['list'])
        current_page += 1
    return article_list


def get_article(article_id, cookie):
    url = 'https://blog-console-api.csdn.net/v1/editor/getArticle'
    params = {'id': article_id}
    headers = {'User-Agent': USER_AGENT, 'Cookie': cookie}
    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        print('Failed to get article {}, status code is {}'.format(
            article_id, response.status_code))
        return None
    return response.json()['data']


def normalize_title(title):
    return re.sub(r'[\\/:*?"<>|]', '_', title)


def main():
    parser = argparse.ArgumentParser(description='CSDN博客导出工具')
    parser.add_argument('--username', help='CSDN用户名')
    parser.add_argument('--cookie-file', help='存储登录cookie的文件')
    parser.add_argument('--interval', type=int, default=2, help='文章爬取间隔，单位：秒')
    parser.add_argument('--output-dir', help='输出目录')
    args = parser.parse_args()

    with open(args.cookie_file) as f:
        cookie = f.read()
    output_dir = pathlib.Path(args.output_dir).resolve()

    article_list = get_article_list(args.username)
    print('Successfully get article list: {} articles'.format(len(article_list)))

    for article in article_list:
        if article_content := get_article(article['articleId'], cookie):
            filename = output_dir / (normalize_title(article['title']) + '.md')
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(article_content['markdowncontent'])
            article['categories'] = article_content['categories']
            article['tags'] = article_content['tags']
            print('Successfully saved article {}'.format(article['title']))
            time.sleep(args.interval)

    with open(output_dir / 'articles.json', 'w', encoding='utf-8') as f:
        json.dump(article_list, f, ensure_ascii=False)
        print('Article infos saved to {}'.format(f.name))


if __name__ == '__main__':
    main()
