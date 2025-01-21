import sys
import time
import requests
from bs4 import BeautifulSoup

from lensScrape import fetch_lens_info

# 将标准输出的编码设置为UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# 设置第一层的URL和筛选条件
base_url = "https://www.pentaxforums.com/lensreviews/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
}

# 代理设置
proxies = {
    'http': 'socks5://127.0.0.1:7890',
    'https': 'socks5://127.0.0.1:7890',
}

# 获取网页内容
def fetch_page(url):
    try:
        response = requests.get(url, headers=headers, proxies=proxies, verify=True)
        response.raise_for_status()  # 如果请求失败，抛出异常
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        sys.exit(1)

# 从首页内容中提取符合条件的超链接
def extract_category_links(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    categories = soup.find_all('span', class_='smallfont')

    filtered_catagories = []
    
    for category in categories:
        link = category.find('a')
        if link:
            category_name = link.text.strip()
            if 'Lenses' in category_name or 'Primes' in category_name:
                filtered_catagories.append({
                    'name': category_name,
                    'link': link['href']
                })      
    
    return filtered_catagories

# 进入第二层网页（镜头列表）
def process_category(category_links):
    # 输出提取的链接
    # for category in category_links:
    for idx, category in enumerate(category_links):
        # print(f"Category: {category['name']} - Link: {category['link']}")
        print(f"当前爬取的网页：{category['link']}")
        # if idx == 4:
        #     break
        process_lens(category)

# 从镜头列表页提取信息
def extract_lens_links(lens_content):
    soup = BeautifulSoup(lens_content, 'html.parser')

    tables = soup.find_all('table', class_='tborder innertable_showcat postbit')
    lens_table = tables[-1]
    lens_list = lens_table.find_all('span', class_='normal')

    lens_links = []

    for lens in lens_list:
        link = lens.find('a')
        if link:
            lens_name = link.text.strip()
            lens_links.append({
                'name': lens_name,
                'link': link['href']
            })

    return lens_links

# 处理镜头
def process_lens(category):
    lens_content = fetch_page(category['link'])
    lens_links = extract_lens_links(lens_content)

    for num, lens in enumerate(lens_links):
    #     if num == 2:
    #         break
        print(f"|{num}----Lens: {lens['name']} - Link: {lens['link']}")

        lens_info = fetch_page(lens['link'])
        fetch_lens_info(lens_info, lens['link'])
        time.sleep(1)

def main():
    # 获取首页内容
    page_content = fetch_page(base_url)

    # 提取符合条件的超链接
    category_links = extract_category_links(page_content)
    # category_links = [{'name': 'M42 Screwmount Extreme Wide-Angle Primes', 'link': 'https://www.pentaxforums.com/lensreviews/Pentax-Takumar-M42-Screwmount-Extreme-Wide-Angle-Primes-c19.html'}]
    
    # 进入第二层网页（镜头列表）
    process_category(category_links)

if __name__ == '__main__':
    main()