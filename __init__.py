import django
import os
import sys

print(django.get_version())

filePath = '/home/haoshuai/文档/django/mysite/upload/file/2020-06-09_01-19-36_的屏幕截图.png' #path + '/' + str(self.file_path)
fsize = os.path.getsize(filePath)
print(fsize)