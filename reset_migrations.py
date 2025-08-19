import os
import sys
import django
"""
重置Django数据库迁移脚本

"""
# 设置Django环境
sys.path.append(os.path.join(os.path.dirname(__file__), 'learn_sail'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learn_sail.settings')
django.setup()

from django.db import connection

# 清除迁移历史记录
def reset_migrations():
    print("正在清除数据库中的迁移历史记录...")
    with connection.cursor() as cursor:
        # 删除所有迁移记录
        cursor.execute("DELETE FROM django_migrations;")
        print("迁移历史记录已清除。")

if __name__ == '__main__':
    reset_migrations()
    print("迁移历史已重置，现在可以重新生成迁移文件。")