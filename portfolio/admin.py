from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SkillCategory, Skill, Project, TimelineEvent,
    ContactMessage, Service, SiteSettings
)


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    search_fields = ['name']
    ordering = ['order', 'name']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_featured', 'order']
    list_filter = ['category', 'is_featured']
    search_fields = ['name']
    list_editable = ['order', 'is_featured']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'is_featured', 'order', 'created_at']
    list_filter = ['status', 'is_featured']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_featured', 'status']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'short_description', 'description')
        }),
        ('Details', {
            'fields': ('tech_stack', 'status', 'is_featured', 'order')
        }),
        ('Media', {
            'fields': ('image', 'live_url', 'repo_url')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'organization', 'event_type', 'start_date', 'is_present', 'order']
    list_filter = ['event_type', 'is_present']
    search_fields = ['title', 'organization', 'description']
    list_editable = ['order']
    ordering = ['-start_date']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['name', 'email', 'subject', 'message', 'created_at']
    actions = ['mark_as_read']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['title', 'description']


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['key', 'value_preview']
    search_fields = ['key', 'value']
    
    def value_preview(self, obj):
        return obj.value[:50] + '...' if len(obj.value) > 50 else obj.value
    value_preview.short_description = 'Value'
