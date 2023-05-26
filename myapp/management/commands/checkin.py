from datetime import datetime
from django.core.management.base import BaseCommand
from myapp.models import Checkin
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
    help = 'Server Manager'
    
    def add_arguments(self, parser):
        parser.add_argument('action', choices=['update', 'delete'], help='Specify the action: update or delete')

    def handle(self, *args, **options):
        print(args)
        action = options['action']
        if action == 'update':
            self.update_commit_logs()
        elif action == 'delete':
            self.delete_commit_logs()
        
        

    def update_commit_logs(self):
        
        self.stdout.write(self.style.SUCCESS("完成日志更新!"))

    def delete_commit_logs(self):
        # 删除所有日志更新
        Checkin.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('删除所有打卡记录.'))