import os
import requests
import re
from datetime import datetime

# MediaWiki API URL
# 请只更改Wiki URL部分为你的Wiki域名
API_URL = "https://Wiki URL/api.php"

def fetch_all_pages(namespaces):
    pages = []
    for namespace in namespaces:
        params = {
            "action": "query",
            "list": "allpages",
            "apnamespace": namespace,
            "aplimit": "max",
            "format": "json"
        }
        while True:
            response = requests.get(API_URL, params=params).json()
            pages.extend(response["query"]["allpages"])
            if "continue" in response:
                params.update(response["continue"])
            else:
                break
    return pages

def export_page(page_title):
    params = {
        "action": "query",
        "titles": page_title,
        "export": "true",
        "format": "xml"
    }
    response = requests.get(API_URL, params=params)
    return response.text

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', '-', filename)

def sanitize_xml_content(xml_content):
    xml_content = xml_content.replace("&lt;", "<").replace("&gt;", ">")
    return xml_content

# 获取当前时间
current_time = datetime.now().strftime('%Y%m%d_%H%M%S')

# 获取wiki域名
wiki_domain = API_URL.split("//")[1].split("/")[0]

# 创建保存路径
save_path = f"D:\\{wiki_domain}_{current_time}"

# 确保保存路径存在
os.makedirs(save_path, exist_ok=True)

# 指定多个命名空间
namespaces = [0, 1, 2]  # 可以根据需要添加更多命名空间

all_pages = fetch_all_pages(namespaces)
for page in all_pages:
    page_title = page['title']
    xml_data = export_page(page_title)
    xml_data = sanitize_xml_content(xml_data)
    filename = sanitize_filename(page_title) + ".xml"
    file_path = os.path.join(save_path, filename)
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(xml_data)
        print(f"导出完成: {file_path}")
    except FileNotFoundError as e:
        print(f"文件保存失败: {e}")
    except Exception as e:
        print(f"发生其他错误: {e}")

print("所有页面导出完成。")
