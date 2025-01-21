import sys
import csv
import re
import requests
from pathlib import Path
from bs4 import BeautifulSoup

# 将标准输出的编码设置为 UTF-8
sys.stdout.reconfigure(encoding='utf-8')

def fetch_lens_info(lens_info, link):

    soup = BeautifulSoup(lens_info, 'html.parser')

    # 依次获取镜头详情页内的所有需要的数据
    lens_name = get_lens_name(soup)
    lens_attributes = get_lens_attributes(soup)
    lens_reviews = get_lens_reviews(soup)
    lens_description = get_lens_description(soup)
    image_url = get_lens_image_info(soup)

    write_to_csv(lens_name, lens_attributes, lens_reviews, lens_description, image_url, link)
    print(f"完成当前镜头爬取与读写")

def get_lens_name(soup):
    try:  
        # 提取镜头信息
        lens_name_tag = soup.find('h1', class_='itemproductname')
        
        if lens_name_tag:
            lens_name = lens_name_tag.text.strip()
            # print(f"镜头名称: {lens_name}")
            return lens_name
        else:
            print("未找到镜头名称")
            return None # 如果没有找到镜头名称，返回None
    
    except Exception as e:
        # 捕获异常并打印错误信息
        print(f"获取镜头名称时出错：{e}")
        return None # 发生错误时返回None

def get_lens_attributes(soup):
    attribute_return_data = {}
    # 提取镜头属性（如锐度、畸变、焦外等）
    attributes = soup.find_all('td', width='75')

    attribute_names = ['sharpness', 'aberration', 'bokeh', 'autofocus', 'handling', 'value']
    temp_attributes = []

    for idx, attribute in enumerate(attributes):
        attribute_name = attribute.text.strip()
        attribute_value_tag = attribute.find_next_sibling('td')

        if attribute_value_tag:
            attribute_value = attribute_value_tag.text.strip()
            # print(f"{attribute_name}: {attribute_value}")
            temp_attributes.append((attribute_name, attribute_value))
        else:
            print("未找到镜头属性")

    # 如果提取到的属性只有5个，插入 'autofocus': '0' 到第四个位置
    if len(temp_attributes) == 5:
        temp_attributes.insert(3, ('autofocus', '0'))

    # 将结果转换为字典
    for name, value in temp_attributes:
        attribute_return_data[name] = value

    return attribute_return_data

def get_lens_reviews(soup):
    reviews_return_data = {}
     # 提取用户评价、平均价格和评分
    review_sections = soup.find_all('table', cellpadding='2', cellspacing='1')

    if len(review_sections) > 0:
        review_data = review_sections[0].find_all('td', class_='alt1', align='center')
        if len(review_data) >= 6:
            reviews_return_data['reviews'] = review_data[3].text.strip()
            reviews_return_data['views'] = review_data[4].text.strip()
            reviews_return_data['last_review_date'] = review_data[5].text.strip()

    if len(review_sections) > 1:
        rating_data = review_sections[1].find_all('td', class_='alt1', align='center')
        if len(rating_data) >= 6:
            reviews_return_data['recommended_by'] = rating_data[3].text.strip()
            reviews_return_data['average_price'] = rating_data[4].text.strip()
            reviews_return_data['average_user_rating'] = rating_data[5].text.strip()
    return reviews_return_data

def get_lens_description(soup):
    itemdescrow = soup.find(id="itemdescrow")
    if itemdescrow:
        smallfont_divs = itemdescrow.find_all('div', class_='smallfont')

        description_text = ""
        for div in smallfont_divs:
            for table in div.find_all('table'):
                table.decompose()
            
            # 获取纯文本，分隔符为" "，并去除首尾空白字符
            description_text += div.get_text(separator=" ", strip=True) + "\n"
        
        # 清理可能的非法字符或多余的空格
        description_text = re.sub(r'\s+', ' ', description_text)  # 替换多个空格为单个空格
        description_text = description_text.strip()  # 去除首尾空白字符

        # print(f"description: {description_text}")
        return description_text
    else:
        print("未找到镜头描述")
        return None # 如果没有找到镜头描述，返回None

def get_lens_image_info(soup):
    try:
        # 找到 itemimage 标签下的 img 标签
        item_image_tag = soup.find('td', id='itemimage')
        if item_image_tag:
            img_tag = item_image_tag.find('img')
            if img_tag:
                image_url = img_tag.get('src', '')
                return image_url
        return None
    except Exception as e:
        print(f"获取镜头图片信息时出错：{e}")
        return None

def write_to_csv(lens_name, lens_attributes, lens_reviews, lens_description, image_url, link):
    # 路径设置    
    current_dir = Path(__file__).resolve().parent
    target_dir = current_dir.parent / 'graph_db' / 'raw_data'
    target_dir.mkdir(parents=True, exist_ok=True)
    csv_file = target_dir / 'Lens.csv'

    with open(csv_file, mode='a', newline='', encoding='utf-8') as file: # 编码选择utf-8，而不是windows-1252
        writer = csv.writer(file)

        # 写入表头，检查文件是否为空来避免重复写入表头
        if file.tell() == 0:
            # 定义Lenses.csv的抬头
            header = [
                'lens_id', 'lens_name',  'mount', 'focal_length',	
                'sharpness', 'aberration', 'bokeh', 'autofocus', 'handling', 'value',
                'reviews', 'views', 'last_date', 'recommended_by', 'price', 'rating',
                'description', 'image_link', 'lens_link']
            writer.writerow(header)
        
        # 格式化数据为列表形式
        row = [
            '',
            lens_name,
            '',
            '',
        ]

        row.extend([lens_attributes.get(key, '') for key in lens_attributes])
        row.extend([lens_reviews.get(key, '') for key in lens_reviews])
        row.append(lens_description)
        row.append(image_url)
        row.append(link)

        writer.writerow(row)
