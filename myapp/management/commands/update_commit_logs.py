from datetime import datetime
from django.core.management.base import BaseCommand
from myapp.models import CommitLog
import subprocess

def custom_date_parser(date_str):
    # 自定义解析日期字符串的方法
    # 根据你的日期字符串格式进行解析，示例中的格式为 "Thu May 25 11:51:32 2023 +0800"
    format_str = "%a %b %d %H:%M:%S %Y %z"
    try:
        date = datetime.strptime(date_str, format_str)
        return date
    except ValueError:
        # 如果解析失败，可以根据实际情况返回默认值或者抛出异常
        return None
    
class Command(BaseCommand):
    help = 'Update commit logs'
    
    def handle(self, *args, **options):
        # 使用Git命令获取提交记录
        result = subprocess.run(['git', 'log', '--pretty=format:%an|%ad|%s'], capture_output=True, text=True)
        # 解析提交记录并保存到提交日志模型中
        commit_logs = result.stdout.split('\n')
        for log in commit_logs:
            if log:
                author, date, message = log.split('|')
                date = custom_date_parser(date)
                # 检查是否已存在相同的记录
                if not CommitLog.objects.filter(author=author, date=date, message=message).exists():
                    CommitLog.objects.create(author=author, date=date, message=message)
        
        print(datetime.now(),"完成日志更新!")

    