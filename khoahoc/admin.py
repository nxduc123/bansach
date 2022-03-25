from django.contrib import admin
from django import forms
from .models import  Category, Course, Lesson, Tag
from django.utils.html import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget

#ckedittoer thêm vào form của lesson
class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Lesson
        fields = '__all__'

class LessonTagInline(admin.TabularInline):
    model = Lesson.tags.through

class LessonAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('/static/css/main.css',)
        }
    form = LessonForm
    list_display = ["id", "subject", "created_date", "active", "course"]
    search_fields = ["subject", "created_date", "course__subject"]
    list_filter = ["subject", "course__subject"]
    readonly_fields = ["avatar"]
    inlines = (LessonTagInline, )
#'''thêm 1 trường vào quản trị  lesonadmin'''
    readonly_fields = ["avatar"]
    def avatar(self, lesson):
        return mark_safe("<img src='/static/{img_url}' alt='{alt}' width=150px />".format(img_url=lesson.image.name, alt=lesson.subject))

class LessonInline(admin.StackedInline):
    model = Lesson
    pk_name = 'course'

class CourseAdmin(admin.ModelAdmin):
    inlines = (LessonInline, )
class CourseAppAdminSite(admin.AdminSite):
    site_header = 'Hệ Thống Khóa Học'
    def get_urls(self):
        return [
            path('course-starts', self.counse_starts())
        ] + super().get_urls()
    def counse_starts(self, request):
        return "Thong Ke"

admin_site = CourseAppAdminSite('mycourse')
# Register your models here
admin_site.register(Category)
admin_site.register(Course, CourseAdmin)
admin_site.register(Tag)
admin_site.register(Lesson, LessonAdmin)

