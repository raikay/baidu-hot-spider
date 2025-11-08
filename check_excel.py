import os
import json
import openpyxl
from datetime import datetime

def get_history_excel():
    """获取最新的历史汇总Excel文件"""
    # 查找百度热搜历史文件
    files = [f for f in os.listdir('.') if f.startswith('baidu_hot_history') and f.endswith('.xlsx')]
    if not files:
        print("未找到历史Excel文件")
        return None
    
    # 按文件名排序，最新的备份文件可能排在后面
    files.sort()
    
    # 返回主历史文件，如果不存在则返回最新的备份文件
    main_file = "baidu_hot_history.xlsx"
    if os.path.exists(main_file):
        return main_file
    elif files:
        return files[-1]  # 返回最新的文件
    else:
        return None

def read_excel(filename):
    """读取Excel文件并显示基本信息（支持Selenium爬虫生成的数据）"""
    try:
        # 使用openpyxl读取Excel文件
        workbook = openpyxl.load_workbook(filename)
        worksheet = workbook.active
        print(f"成功读取文件: {filename}")
        print(f"工作表名称: {worksheet.title}")
        
        # 获取所有行数据
        all_rows = list(worksheet.iter_rows(values_only=True))
        if not all_rows:
            print("错误: 文件为空")
            return False
        
        # 获取表头
        headers = all_rows[0]
        print(f"文件包含 {len(all_rows) - 1} 条记录")
        print(f"表头: {', '.join([str(h) for h in headers])}")
        
        # 检查是否包含'爬取时间'和'JSON数据'列
        has_time_col = False
        has_json_col = False
        time_col_index = -1
        json_col_index = -1
        
        for i, header in enumerate(headers):
            if header and '爬取时间' in str(header):
                has_time_col = True
                time_col_index = i
            if header and 'JSON数据' in str(header):
                has_json_col = True
                json_col_index = i
        
        if not has_time_col or not has_json_col:
            print("错误: 文件格式不正确，缺少必要的列")
            return False
        
        # 显示最近的2条爬取记录
        print("\n最近的2条爬取记录:")
        records_to_show = min(2, len(all_rows) - 1)
        rows_to_show = all_rows[-records_to_show:]
        
        for row_idx, row in enumerate(rows_to_show, max(1, len(all_rows) - records_to_show)):
            if len(row) > max(time_col_index, json_col_index):
                crawl_time = row[time_col_index] if time_col_index < len(row) else "N/A"
                json_data_str = row[json_col_index] if json_col_index < len(row) else ""
                
                print(f"时间: {crawl_time}")
                try:
                    # 尝试解析JSON数据
                    if json_data_str:
                        json_data = json.loads(json_data_str)
                        print(f"  包含 {len(json_data)} 条热搜数据")
                        
                        # 验证数据结构
                        if json_data and isinstance(json_data[0], dict):
                            # 显示前两条热搜的信息
                            for j, hot_item in enumerate(json_data[:2], 1):
                                title = hot_item.get('title', '无标题')
                                hot_index = hot_item.get('hot_index', '无指数')
                                rank = hot_item.get('rank', j)
                                print(f"  {rank}. {title} - 指数: {hot_index}")
                        else:
                            print("  数据格式不符合预期，但成功解析JSON")
                            print(f"  数据预览: {json_data[:2] if len(json_data) >= 2 else json_data}")
                    else:
                        print("  JSON数据为空")
                except json.JSONDecodeError as e:
                    print(f"  JSON数据解析失败: {str(e)}")
                    # 尝试显示部分数据进行调试
                    json_preview = str(json_data_str)[:100] + '...' if len(str(json_data_str)) > 100 else str(json_data_str)
                    print(f"  数据预览: {json_preview}")
                except Exception as e:
                    print(f"  处理JSON数据时发生错误: {str(e)}")
        
        # 验证数据完整性
        print("\n数据完整性检查:")
        valid_records = 0
        total_records = len(all_rows) - 1  # 减去表头行
        
        for row in all_rows[1:]:  # 跳过表头行
            if len(row) > json_col_index:
                json_data_str = row[json_col_index] if json_col_index < len(row) else ""
                try:
                    if json_data_str:
                        json_data = json.loads(json_data_str)
                        if isinstance(json_data, list) and len(json_data) > 0:
                            valid_records += 1
                except:
                    pass
        
        print(f"有效记录数: {valid_records}/{total_records}")
        
        return True
    except Exception as e:
        print(f"读取Excel文件失败: {e}")
        return False

def check_file_existence():
    """检查是否有Selenium爬虫生成的数据文件"""
    history_file = "baidu_hot_history.xlsx"
    backup_files = [f for f in os.listdir('.') if f.startswith('baidu_hot_history_backup') and f.endswith('.xlsx')]
    
    print("\n文件检查:")
    print(f"历史文件存在: {os.path.exists(history_file)}")
    if os.path.exists(history_file):
        file_size = os.path.getsize(history_file) / 1024  # KB
        print(f"历史文件大小: {file_size:.2f} KB")
    
    print(f"备份文件数量: {len(backup_files)}")
    if backup_files:
        backup_files.sort(reverse=True)  # 最新的备份文件在前面
        print(f"最新备份文件: {backup_files[0]}")

def main():
    """主函数"""
    print(f"开始检查Excel文件 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("(支持Selenium爬虫生成的数据格式)")
    
    # 检查文件存在性
    check_file_existence()
    
    # 获取最新的历史文件
    filename = get_history_excel()
    if not filename:
        print("错误: 未找到可检查的Excel文件")
        print("请先运行baidu_hot_spider_selenium.py脚本爬取数据")
        return False
    
    # 读取并验证文件
    success = read_excel(filename)
    
    if success:
        print(f"\n检查完成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("数据格式符合Selenium爬虫的输出要求")
    else:
        print(f"\n检查失败 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return success

if __name__ == "__main__":
    main()
