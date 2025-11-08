import schedule
import time
import subprocess
import os
from datetime import datetime

def run_spider():
    """运行爬虫任务"""
    print(f"定时任务启动 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        # 直接导入并运行爬虫模块
        from baidu_hot_spider import main
        main()
        print(f"爬虫执行完成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        print(f"爬虫运行失败: {e}")
        # 记录错误到日志文件
        with open("spider_error.log", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 错误: {e}\n")
        # 添加短暂延迟避免频繁失败
        time.sleep(5)

def main():
    """主函数，设置定时任务"""
    print("百度热搜榜定时爬虫已启动")
    print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("设置为每分钟爬取一次")
    print("按 Ctrl+C 停止程序")
    
    # 设置定时任务，每10分钟执行一次
    schedule.every(10).minute.do(run_spider)
    
    # 立即执行一次
    run_spider()
    
    # 持续运行，等待定时任务执行
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次是否有待执行的任务
    except KeyboardInterrupt:
        print("\n程序已停止")

if __name__ == "__main__":
    main()