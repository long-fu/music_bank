from django.db import models
from django.utils.html import format_html
import django.utils.timezone as timezone

import os
import sys

from pymediainfo import MediaInfo
import json

# path = os.path.abspath(os.path.dirname(sys.argv[0]))

class Audio(models.Model):
    
    # 文件路径
    path = models.FileField(upload_to='audio')
    
    # 歌名
    title = models.CharField(max_length=32)
    
    # 作者
    author = models.CharField(max_length=32,default='未知')

    # 歌词
    lyric = models.FileField(upload_to='audio/lyric',null=True,blank=True)
    
    # 歌曲时长
    duration = models.FloatField(default=0.0)
    
    # 比特率
    bit_rate = models.IntegerField(default=0)
    
    # 采样速率
    sample_rate = models.IntegerField(default=0)
    
    # 类型
    media_type = models.CharField(max_length=32,default='未知')
    # 声道
    # channel = models.CharField(max_length=32,default='立体声')
    channel = models.IntegerField(default=0)

    # 类型 流派
    genre = models.CharField(max_length=64,default='未知')

    # 专辑图片
    # cover = models.FileField(upload_to='audio/image',null=True,blank=True)
    cover = models.ImageField(upload_to='audio/images',null=True,blank=True)
    # 专辑名
    album = models.CharField(max_length=64,null=True,blank=True)

    # 文件大小
    size = models.FloatField(default=0.0)

    # 录制日期
    recorded_date = models.CharField(max_length=16,default='2022')

    # 文件添加时间
    pub_time = models.DateTimeField('time published',auto_now_add=True)

    # 文件打开一次记录一次的时间
    open_time = models.DateTimeField('time opened',auto_now=True)

    open_count = models.IntegerField(default=0)


    def save(self,*args, **kwargs):

        duration = 0
        bit_rate = 0
        genre = '未知'
        title = ''
        album = '未知'
        sampling_rate = 0
        channels = 0
        recorded_date = '2022'
        internet_media_type = '未知'
        performer = '未知'

        media_info = MediaInfo.parse(self.path).to_json()
        # print(media_info)
        media_info = json.loads(media_info)
        tracks = media_info["tracks"]

        for track in tracks:
            track_type = track["track_type"]
            if track_type == 'General':
                duration = track['duration']
                title = track.get('title','')
                genre = track.get('genre','未知')
                recorded_date = track.get('recorded_date','2022')
                album = track.get('album','未知')
                internet_media_type = track.get('internet_media_type','audio/mpeg')
                performer = track.get('performer','未知')
                pass
            elif track_type == 'Audio':
                duration = track['duration']
                bit_rate = track['bit_rate']
                channels = track['channel_s']
                sampling_rate = track['sampling_rate']
                internet_media_type = track.get('internet_media_type','audio/mpeg')
                pass
            else:
                assert()
                pass
            # print(type(track_type),track_type)
            pass

        
        # 歌曲标题
        if title != '':
            self.title = title

        # 专辑
        if album != '未知':
            self.album = album

        # 作者
        if performer != '未知':
            self.author = performer

        # 一定存在的数据
        self.duration = duration

        self.bit_rate = bit_rate

        self.channel = channels

        self.sample_rate = sampling_rate
        
        self.size = self.path.size

        # 存在默认值 

        # 歌曲类型
        self.genre = genre
        
        self.media_type = internet_media_type

        self.recorded_date = recorded_date

        super(Audio, self).save(*args, **kwargs)
        

        pass
    def cover_image(self):
        return format_html(
            '<img src="/media/{}" height="64px" width="64px" />', 
            self.cover,
            )
        pass
    pass

# from filer.fields.image import FilerImageField
# Create your models here.
class File(models.Model):
    # 文件地址
    # file_path = models.CharField(max_length=1000,unique=True,null=False)
    file_path = models.FileField(upload_to='file',unique=True)
    # 文件名
    file_name = models.CharField(max_length=32)
    # 扩展文件(音乐 歌词文件) 字幕 文件
    link_path = models.FileField(upload_to='link',null=True,blank=True)
    # 文件类型(mp3,ava,mp4,字符串)
    file_type = models.CharField(max_length=16,default='none')
    # 文件时常 
    duration = models.FloatField(default=0.0)
    # 文件封面
    image_path = models.ImageField(upload_to='thumb',null=True,blank=True)
    # 文件大小
    file_size = models.FloatField(default=0.0)
    # 文件添加时间
    pub_time = models.DateTimeField('time published',auto_now_add=True)
    # 文件打开一次记录一次的时间
    open_time = models.DateTimeField('time opened',auto_now=True)


    def make_thumb(path, size = 480):
        pixbuf = Image.open(path)
        width, height = pixbuf.size

        if width > size:
            delta = width / size
            height = int(height / delta)
            pixbuf.thumbnail((size, height), Image.ANTIALIAS)

            return pixbuf
    # 重载save
    def save(self,*args, **kwargs):
        file_name,file_type = os.path.splitext(str(self.file_path))
        # print(file_name,file_type)
        self.file_size = self.file_path.size
        self.file_name = file_name
        self.file_type = file_type
        super(File, self).save(*args, **kwargs)

        # 生成封面图片

        # 音乐文件

        # 视频文件

        pass

    # 封面  
    def image(self):

        return format_html(
            '<img src="/media/{}" height="64px" width="64px" />', 
            self.image_path,
            )
    
    image.short_description = '封面'

    pass