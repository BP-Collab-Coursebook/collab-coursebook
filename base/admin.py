from base.models import Course, Category, Period, Topic, Content, CourseStructureEntry, Tag
from .models import Profile

from django.contrib import admin


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'period']
    exclude = ['creation_date']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ['title', 'start', 'end']


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    exclude = ['creation_date', 'preview']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(CourseStructureEntry)
class CourseStructureAdmin(admin.ModelAdmin):
    list_display = ['index', 'course', 'topic']
    list_filter = ['course']
