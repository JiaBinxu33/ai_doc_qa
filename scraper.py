# 导入所需的库
import requests  # 用于发送 HTTP 请求，从网页获取 HTML 内容
from bs4 import BeautifulSoup  # 用于解析 HTML，方便地提取所需数据
import json  # 用于处理 JSON 数据，这里是把我们抓取的数据保存为 JSON 文件
from urllib.parse import urljoin # 用于拼接 URL，将相对路径转换为绝对路径

def scrape_fastapi_docs():
    """
    主函数，用于爬取 FastAPI 官方文档的教程部分，并将内容保存为 JSON 文件。
    """
    # --- 第 1 步：准备工作与获取所有导航链接 ---

    # 定义基础 URL 和起始页面 URL
    base_url = "https://fastapi.tiangolo.com"
    start_url = "https://fastapi.tiangolo.com/tutorial/"

    print("开始爬取 FastAPI 文档...")
    print(f"从起始页面获取所有导航链接: {start_url}")

    try:
        # 发送 GET 请求到教程首页
        response = requests.get(start_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"无法获取起始页面 {start_url}。错误: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    # 使用稳定的 class="md-sidebar--primary" 来定位整个侧边栏
    navigation = soup.find('div', class_="md-sidebar--primary")

    page_urls = set()
    if navigation:
        # 找到导航栏里所有的 <a> 标签
        links = navigation.find_all('a', class_="md-nav__link")
        for link in links:
            href = link.get('href')
            if href:
                full_url = urljoin(start_url, href)
                page_urls.add(full_url)
    
    page_urls = list(page_urls)

    if not page_urls:
        print("错误：未能从页面上发现任何文档链接。可能是网站结构再次改变，请检查爬虫代码。")
        return

    print(f"成功发现 {len(page_urls)} 个文档页面链接。")


    # --- 第 2 步：遍历链接，抓取每个页面的标题和正文 ---
    
    docs = [] 
    print("\n开始逐个抓取页面内容...")

    for url in page_urls:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            page_soup = BeautifulSoup(response.content, 'html.parser')
            
            title_tag = page_soup.find('h1')
            # 数据清洗
            title = title_tag.get_text(strip=True) if title_tag else "无标题"
            
            # 原来的 'div', attrs={"role": "main"} 在某些页面上不存在。
            # 我们换成更通用的 <main> 标签，这个标签在所有文档页面上都存在。
            content_div = page_soup.find("main")

            # 数据清洗
            content = content_div.get_text(separator='\n', strip=True) if content_div else ""
            
            if content:
                doc_data = {
                    "url": url,
                    "title": title,
                    "content": content
                }
                docs.append(doc_data)
                print(f"  [成功] 抓取: {title}")
            else:
                # 理论上，使用 <main> 标签后，这个警告应该不会再出现了
                print(f"  [警告] 在页面 {url} 未找到正文内容。")

        except requests.RequestException as e:
            print(f"  [失败] 抓取页面 {url} 时出错: {e}")
            
    # --- 第 3 步：将抓取到的所有数据存储为 JSON 文件 ---

    print("\n所有页面抓取完毕，正在将数据保存到文件...")
    
    with open('fastapi_docs.json', 'w', encoding='utf-8') as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)
        
    print(f"任务完成！成功将 {len(docs)} 篇文档保存到 fastapi_docs.json 文件中。")

if __name__ == "__main__":
    scrape_fastapi_docs()

