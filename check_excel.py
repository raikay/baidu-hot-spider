import os
import openpyxl
import json
from datetime import datetime

# 获取指定的Excel文件（历史汇总文件）
def get_history_excel():
    filename = "baidu_hot_history.xlsx"
    if not os.path.exists(filename):
        print(f"未找到文件: {filename}")
        # 尝试获取最新的备份文件
        backup_files = [f for f in os.listdir('.') if f.startswith('baidu_hot_backup_') and f.endswith('.xlsx')]
        if backup_files:
            backup_files.sort()
            filename = backup_files[-1]
            print(f"找到备份文件: {filename}")
        else:
            return None
    return filename

# 读取并显示Excel文件内容
def read_excel(filename):
    try:
        workbook = openpyxl.load_workbook(filename)
        worksheet = workbook.active
        
        print(f"文件: {filename}")
        print("\n表头:")
        # 打印表头（第一行）
        headers = list(worksheet.rows)[0]
        for cell in headers:
            print(f"{cell.value}", end="\t")
        print("\n")
        
        # 获取数据行数
        data_rows = list(worksheet.iter_rows(min_row=2))
        print(f"总数据条数: {len(data_rows)}")
        print("\n最近2条爬取记录:")
        
        # 显示最近的2条记录
        for i, row in enumerate(data_rows[-2:], max(1, len(data_rows)-1)):
            values = [cell.value for cell in row]
            if len(values) >= 2:
                print(f"\n爬取时间 {i}: {values[0]}")
                print(f"JSON数据预览:")
                try:
                    # 尝试解析JSON数据并显示前几条热搜
                    json_data = json.loads(values[1])
                    print(f"  - 共包含 {len(json_data)} 条热搜数据")
                    # 显示前3条热搜数据
                    for j, hot_item in enumerate(json_data[:3], 1):
                        print(f"  {j}. 标题: {hot_item.get('title', '无标题')}")
                        print(f"     指数: {hot_item.get('hot_index', '无指数')}")
                except json.JSONDecodeError:
                    print(f"  - JSON数据长度: {len(values[1])} 字符")
                    print(f"  - 数据前100字符: {values[1][:100]}...")
        
    except Exception as e:
        print(f"读取Excel文件失败: {e}")

if __name__ == "__main__":
    history_file = get_history_excel()
    if history_file:
        read_excel(history_file)
