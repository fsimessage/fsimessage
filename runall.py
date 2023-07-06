#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import time
from threading import Thread

def run_python_file(file_path):
    python_path = '/usr/bin/python3.11'  # 替换为实际的Python 3.11可执行文件路径
    process = subprocess.Popen([python_path, file_path])
    
    # 等待子进程结束，设置超时时间为1分钟
    process.communicate(timeout=60)

def run_all_python_files():
    current_dir = os.getcwd()
    current_file = os.path.basename(__file__)
    files = [file_name for file_name in os.listdir(current_dir) if file_name.endswith('.py') and file_name != current_file]

    threads = []

    for file_name in files:
        file_path = os.path.join(current_dir, file_name)
        thread = Thread(target=run_python_file, args=(file_path,))
        thread.start()
        threads.append(thread)

    # 等待所有线程执行完毕
    for thread in threads:
        thread.join()

# 每分钟执行一次循环
while True:
    run_all_python_files()
    time.sleep(60)


# import os
# import subprocess

# def run_all_python_files():
#     current_dir = os.getcwd()
#     current_file = os.path.basename(__file__)
#     files = [file_name for file_name in os.listdir(current_dir) if file_name.endswith('.py') and file_name != current_file]

#     python_path = '/usr/bin/python3.11'  # 替换为实际的Python 3.11可执行文件路径

#     for file_name in files:
#         # 启动子进程执行Python文件，指定使用Python 3.11版本
#         process = subprocess.Popen([python_path, file_name])

# run_all_python_files()























# import os
# import time
# # 获取当前文件夹路径
# while 1:
  
#   folder_path = os.getcwd()
  
#   # 获取当前Python文件的文件名
#   current_file = os.path.basename(__file__)
  
#   # 遍历当前文件夹下所有文件
#   for file_name in os.listdir(folder_path):
#       # 如果文件以.py结尾且不是当前文件
#       if file_name.endswith('.py') and file_name != current_file:
#           # 构造要执行的命令
#           command = f'python3.11 {file_name}'
#           # 执行命令
#           os.system(command)
#   time.sleep(60)
