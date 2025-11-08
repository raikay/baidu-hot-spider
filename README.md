# 百度热搜榜爬虫项目

## 项目介绍

本项目是一个功能完善的百度热搜榜爬虫系统，可以定时爬取百度热搜榜数据，并将数据以JSON格式保存到Excel文件中。项目具有以下特点：

- 自动化爬取百度热搜榜前20条数据
- 精确提取标题、简介和热搜指数
- 将数据转换为JSON格式并追加到同一个Excel文件
- 支持定时任务，可设置固定频率自动爬取
- 具备错误处理和数据验证机制
- 提供数据查询和展示功能

## 环境准备

### 所需软件

- Python 3.6 或更高版本
- pip 包管理工具

### 依赖库安装

项目依赖以下Python库，可以通过 requirements.txt 一键安装：

```bash
pip install -r requirements.txt
```

主要依赖库包括：
- requests：用于发送HTTP请求
- beautifulsoup4：用于解析HTML
- openpyxl：用于操作Excel文件
- schedule：用于设置定时任务

## 项目结构

```
pco/
├── baidu_hot_spider.py     # 核心爬虫模块
├── schedule_spider.py      # 定时任务模块
├── check_excel.py          # 数据验证模块
├── requirements.txt        # 依赖库列表
├── baidu_hot_history.xlsx  # 数据存储文件
└── README.md               # 项目说明文档
```

## 核心功能实现

### 1. 爬虫模块 (baidu_hot_spider.py)

爬虫模块负责从百度热搜榜页面获取数据并保存。主要包含以下函数：

#### fetch_baidu_hot 函数

```python
def fetch_baidu_hot():
    """爬取百度热搜榜数据"""
    url = "https://top.baidu.com/board?tab=realtime"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        
        # 获取所有热搜卡片容器
        hot_list = soup.select('.category-wrap_iQLoo tbody')
        if hot_list:
            # 从tbody中获取所有行
            rows = hot_list[0].find_all('tr')[:20]  # 取前20个
            
            # 获取所有热搜指数元素
            hot_indices = soup.select('.hot-index_1Bl1a')
            
            for i, row in enumerate(rows, 1):
                # 从当前行获取标题
                title_element = row.select_one('.c-single-text-ellipsis')
                title = title_element.get_text().strip() if title_element else "无标题"
                
                # 从当前行获取简介
                desc_element = row.select_one('.hot-desc_1m_jR')
                description = desc_element.get_text().strip() if desc_element else "无简介"
                
                # 获取对应的热搜指数
                hot_index = "无指数"
                if i-1 < len(hot_indices):
                    hot_index = hot_indices[i-1].get_text().strip()
                
                results.append({
                    'rank': i,
                    'title': title,
                    'description': description,
                    'hot_index': hot_index
                })
        # ... 备用方法和数据验证代码 ...
        
        return results
    except Exception as e:
        print(f"爬取失败: {e}")
        return []
```

这个函数使用BeautifulSoup解析百度热搜榜页面，通过CSS选择器精确定位标题、简介和热搜指数元素，确保数据准确匹配。

#### save_to_excel 函数

```python
def save_to_excel(data):
    """将爬取的数据转换为JSON并追加到同一个Excel文件中"""
    filename = "baidu_hot_history.xlsx"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 将数据转换为JSON字符串
    json_data = json.dumps(data, ensure_ascii=False, indent=2)
    
    try:
        # 检查文件是否存在
        if os.path.exists(filename):
            # 打开现有文件
            workbook = openpyxl.load_workbook(filename)
            worksheet = workbook.active
        else:
            # 创建新文件和工作表
            workbook = openpyxl.Workbook()
            worksheet = workbook.active
            worksheet.title = "hot_search_history"
            # 设置表头
            worksheet.append(["爬取时间", "JSON数据"])
        
        # 追加新数据行
        worksheet.append([current_time, json_data])
        
        # 调整列宽
        worksheet.column_dimensions['A'].width = 20
        worksheet.column_dimensions['B'].width = 150
        
        # 保存文件
        workbook.save(filename)
        print(f"数据已追加到 {filename} 文件")
        return filename
    except Exception as e:
        # 错误处理和备份机制
        # ...
```

这个函数将爬取的数据转换为JSON格式，并以追加的方式写入到Excel文件中，确保所有历史数据都保存在同一个文件里。

### 2. 定时任务模块 (schedule_spider.py)

定时任务模块负责设置和管理爬虫的自动执行，使用schedule库实现定时功能：

```python
import schedule
import time
import os
from datetime import datetime

# 直接导入并运行爬虫模块
def run_spider():
    """运行爬虫任务"""
    print(f"定时任务启动 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        from baidu_hot_spider import main
        main()
        print(f"爬虫执行完成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        print(f"爬虫运行失败: {e}")
        # 记录错误到日志文件
        with open("spider_error.log", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 错误: {e}\n")
        time.sleep(5)

# 设置定时任务
def main():
    print("百度热搜榜定时爬虫已启动")
    print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("设置为每分钟爬取一次")
    print("按 Ctrl+C 停止程序")
    
    # 设置定时任务，每分钟执行一次
    schedule.every(1).minute.do(run_spider)
    
    # 立即执行一次
    run_spider()
    
    # 持续运行，等待定时任务执行
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次是否有待执行的任务
    except KeyboardInterrupt:
        print("\n程序已停止")
```

### 3. 数据验证模块 (check_excel.py)

数据验证模块用于检查和展示Excel文件中的数据：

```python
import os
import openpyxl
import json
from datetime import datetime

# 获取历史汇总文件
def get_history_excel():
    filename = "baidu_hot_history.xlsx"
    # ... 查找文件逻辑 ...
    return filename

# 读取并显示Excel文件内容
def read_excel(filename):
    try:
        workbook = openpyxl.load_workbook(filename)
        worksheet = workbook.active
        
        print(f"文件: {filename}")
        # ... 显示表头和数据 ...
        
        # 显示最近的记录
        for i, row in enumerate(data_rows[-2:], max(1, len(data_rows)-1)):
            values = [cell.value for cell in row]
            if len(values) >= 2:
                print(f"\n爬取时间 {i}: {values[0]}")
                print(f"JSON数据预览:")
                try:
                    # 解析JSON数据
                    json_data = json.loads(values[1])
                    print(f"  - 共包含 {len(json_data)} 条热搜数据")
                    # 显示部分热搜内容
                    # ...
                except json.JSONDecodeError:
                    # 错误处理
                    # ...
    except Exception as e:
        print(f"读取Excel文件失败: {e}")
```

## 使用方法

### 1. 单次爬取

运行核心爬虫脚本，执行一次爬取任务：

```bash
python baidu_hot_spider.py
```

### 2. 定时爬取

启动定时任务，设置为每10分钟自动爬取一次：

```bash
python schedule_spider.py
```

要停止定时任务，可以按 `Ctrl+C` 中断程序。

### 3. 查看数据

运行数据验证脚本，查看Excel文件中的数据：

```bash
python check_excel.py
```

## 技术要点解析

### 1. 数据提取策略

本项目采用了两种数据提取策略，确保在不同情况下都能准确获取数据：

1. **首选策略**：通过表格结构（tbody > tr）获取每个热搜项目的容器，然后从中提取标题和简介
2. **备用策略**：分别获取内容卡片和热搜指数，然后按顺序匹配

这种双重保障机制大大提高了爬虫的稳定性和准确性。

### 2. 数据存储优化

为了便于数据管理和分析，项目采用了以下存储策略：

1. 将每次爬取的20条热搜数据转换为一个完整的JSON对象
2. 所有爬取记录都追加到同一个Excel文件中
3. 每一行记录包含两个字段：爬取时间和JSON数据

这种设计有以下优势：
- 避免生成大量独立文件
- 便于按时间顺序查看历史数据
- 保持每次爬取的数据完整性
- 方便后续导入到其他系统进行分析

### 3. 错误处理和健壮性

项目包含多层错误处理机制：

1. 网络请求超时处理
2. HTML解析异常捕获
3. Excel文件操作错误处理
4. 自动创建备份文件机制
5. 错误日志记录

这些机制确保了爬虫在面对各种异常情况时能够保持稳定运行。

## 常见问题及解决方案

### 1. 爬取数据为空

**可能原因**：
- 网络连接问题
- 百度热搜榜页面结构发生变化
- 被网站识别为爬虫并拦截

**解决方案**：
- 检查网络连接
- 更新User-Agent
- 调整爬取频率，避免过于频繁
- 检查并更新CSS选择器

### 2. Excel文件保存失败

**可能原因**：
- 文件被其他程序占用
- 磁盘空间不足
- JSON数据过长

**解决方案**：
- 关闭可能占用Excel文件的程序
- 检查磁盘空间
- 程序会自动创建备份文件，确保数据不丢失

### 3. 定时任务停止运行

**可能原因**：
- 遇到未捕获的异常
- 系统重启或进程被终止

**解决方案**：
- 查看spider_error.log日志文件
- 考虑使用系统服务或进程管理工具确保长时间运行

## 项目扩展建议

1. **添加代理IP池**：防止IP被封禁
2. **实现邮件或短信通知**：当特定关键词出现时发送提醒
3. **开发Web界面**：提供可视化的数据展示和管理
4. **增加数据统计功能**：分析热搜词频和热度变化趋势
5. **支持多平台热搜数据采集**：扩展到微博、知乎等平台

## 总结

本项目实现了一个功能完整、稳定可靠的百度热搜榜爬虫系统。通过合理的数据提取策略、优化的存储方式和完善的错误处理机制，确保了系统能够持续稳定地运行并收集高质量的数据。项目结构清晰，代码易于理解和维护，适合作为学习Python爬虫开发的参考案例。

通过运行定时任务，您可以持续收集百度热搜数据，为后续的数据分析和研究提供基础。