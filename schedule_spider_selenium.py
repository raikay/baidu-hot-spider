import time
import schedule
import subprocess
import sys
from datetime import datetime

def run_spider():
    """运行百度热搜榜爬虫脚本"""
    print(f"\n开始定时爬取 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        # 运行Selenium版本的爬虫脚本
        result = subprocess.run([sys.executable, "baidu_hot_spider_selenium.py"], 
                              capture_output=True, 
                              text=True, 
                              timeout=300)  # 设置5分钟超时
        
        # 输出执行结果
        if result.stdout:
            print(f"爬虫输出:\n{result.stdout}")
        if result.stderr:
            print(f"爬虫错误输出:\n{result.stderr}")
        
        # 检查执行状态
        if result.returncode == 0:
            print(f"定时爬取成功完成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"定时爬取失败，返回码: {result.returncode}")
            # 记录错误日志
            log_error(f"爬虫执行失败，返回码: {result.returncode}\n错误输出: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("爬虫执行超时，已强制终止")
        log_error("爬虫执行超时，已强制终止")
    except Exception as e:
        print(f"运行爬虫时发生错误: {str(e)}")
        log_error(f"运行爬虫时发生错误: {str(e)}")
    
    print(f"本次定时爬取处理完毕 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def log_error(error_message):
    """记录错误信息到日志文件"""
    log_filename = f"schedule_error_{datetime.now().strftime('%Y%m%d')}.log"
    try:
        with open(log_filename, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {error_message}\n")
        print(f"错误日志已写入: {log_filename}")
    except Exception as e:
        print(f"写入错误日志失败: {str(e)}")

def setup_schedule(minutes_interval=30):
    """设置定时任务"""
    # 每分钟执行一次（仅用于测试）
    schedule.every(minutes_interval).minutes.do(run_spider)
    print(f"定时任务已设置，每{minutes_interval}分钟执行一次")
    print(f"下次执行时间: {schedule.next_run()}")

def main():
    """主函数"""
    print("百度热搜榜定时爬虫（Selenium版本）启动中...")
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 设置定时任务（默认每30分钟执行一次，测试时可设为1分钟）
    setup_schedule(minutes_interval=1)  # 测试时设置为每分钟执行
    
    # 立即执行一次爬虫
    run_spider()
    
    print("\n定时任务已启动，按Ctrl+C停止")
    
    # 主循环，保持程序运行
    try:
        while True:
            schedule.run_pending()
            time.sleep(10)  # 每10秒检查一次是否有待执行的任务
    except KeyboardInterrupt:
        print("\n定时爬虫已手动停止")
    except Exception as e:
        print(f"定时任务运行时发生错误: {str(e)}")
        log_error(f"定时任务运行时发生错误: {str(e)}")
    finally:
        print(f"程序结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
