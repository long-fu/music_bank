from django.contrib import admin
from .models import File,Audio
# Register your models here.

class AudioAdmin(admin.ModelAdmin):
    readonly_fields = ('duration','bit_rate',
    'sample_rate','channel','size','genre','media_type')

    list_display = ('cover_image', 'album', 'title',
    'author','genre','media_type','channel',
    'bit_rate','sample_rate',
    'duration','size')

    list_filter = ['media_type','channel','genre']
    search_fields = ['title']
    pass

# 后段管理 查看部分
class FileAdmin(admin.ModelAdmin):

    # 因为不需要在后台修改该项，所以设置为只读
    readonly_fields = ('file_type','duration','file_size')

    list_display = ('image', 'file_name', 'file_type','duration',
    'file_size','open_time','pub_time')

    list_filter = ['file_type']

    search_fields = ['file_name']

    # def preview(self,obj):

    #     return '<img src="%s" height="64" width="64" />' % (obj.image_path)


    # preview.allow_tags = True
    # preview.short_description = "图片"


admin.site.register(File, FileAdmin)

admin.site.register(Audio, AudioAdmin)