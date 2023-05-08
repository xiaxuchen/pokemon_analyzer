import os
# 创建lock目录
if not os.path.exists("lock"):
    os.mkdir("lock")

if not os.path.exists("html"):
    os.mkdir("html")
