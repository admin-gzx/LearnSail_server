import os
import sys
import subprocess
"""
重建Django数据库迁移脚本
"""
# 项目根目录
base_dir = os.path.dirname(os.path.abspath(__file__))
# Django项目目录
django_dir = os.path.join(base_dir, 'learn_sail')

# 获取所有应用名称
def get_apps():
    apps = []
    for item in os.listdir(django_dir):
        item_path = os.path.join(django_dir, item)
        if os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, 'models.py')):
            apps.append(item)
    return apps

# 删除迁移文件
def delete_migrations():
    print("正在删除所有迁移文件...")
    for app in get_apps():
        migrations_dir = os.path.join(django_dir, app, 'migrations')
        if os.path.exists(migrations_dir):
            for file in os.listdir(migrations_dir):
                file_path = os.path.join(migrations_dir, file)
                if file != '__init__.py' and os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"已删除: {file_path}")
    print("迁移文件删除完成。")

# 生成迁移文件
def make_migrations():
    print("正在生成迁移文件...")
    os.chdir(django_dir)
    # 先为users应用生成迁移
    subprocess.run(['python', 'manage.py', 'makemigrations', 'users'], check=True)
    # 再为其他应用生成迁移
    subprocess.run(['python', 'manage.py', 'makemigrations'], check=True)
    print("迁移文件生成完成。")

# 应用迁移
def migrate():
    print("正在应用迁移...")
    os.chdir(django_dir)
    # 首先标记所有初始迁移为已应用（不实际执行）
    subprocess.run(['python', 'manage.py', 'migrate', '--fake-initial'], check=True)
    # 然后正常应用迁移
    subprocess.run(['python', 'manage.py', 'migrate'], check=True)
    print("迁移应用完成。")

if __name__ == '__main__':
    delete_migrations()
    make_migrations()
    migrate()