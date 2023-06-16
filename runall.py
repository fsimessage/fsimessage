#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
# 获取当前文件夹路径
while 1:
  
  folder_path = os.getcwd()
  
  # 获取当前Python文件的文件名
  current_file = os.path.basename(__file__)
  
  # 遍历当前文件夹下所有文件
  for file_name in os.listdir(folder_path):
      # 如果文件以.py结尾且不是当前文件
      if file_name.endswith('.py') and file_name != current_file:
          # 构造要执行的命令
          command = f'python {file_name}'
          # 执行命令
          os.system(command)
  time.sleep(60)
