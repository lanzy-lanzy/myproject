from django.db import models


class SkillCategory(models.Model):
    """Category for grouping skills"""
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Skill Categories"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class Skill(models.Model):
    """Individual skill with category"""
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        SkillCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='skills'
    )
    icon = models.CharField(max_length=50, blank=True, help_text="labb icon name (e.g., 'rmx.code')")
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['category__order', 'order', 'name']
    
    def __str__(self):
        return self.name


class Project(models.Model):
    """Portfolio project"""
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
        ('maintained', 'Maintained'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    short_description = models.TextField(max_length=300)
    description = models.TextField(blank=True)
    tech_stack = models.JSONField(default=list, help_text="List of technologies used")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    image = models.ImageField(upload_to='projects/', blank=True)
    live_url = models.URLField(blank=True)
    repo_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    class Meta:
        ordering = ['-is_featured', 'order', '-created_at']
    
    def __str__(self):
        return self.title
    
    def get_status_display_class(self):
        """Return Tailwind class based on status"""
        status_classes = {
            'completed': 'badge-success',
            'in_progress': 'badge-warning',
            'maintained': 'badge-info',
        }
        return status_classes.get(self.status, 'badge-ghost')


class TimelineEvent(models.Model):
    """Career/learning timeline events"""
    EVENT_TYPES = [
        ('education', 'Education'),
        ('work', 'Work Experience'),
        ('certification', 'Certification'),
        ('milestone', 'Milestone'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    organization = models.CharField(max_length=200, blank=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='milestone')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_present = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-start_date', 'order']
    
    def __str__(self):
        return self.title
    
    def get_date_range(self):
        """Return formatted date range"""
        start = self.start_date.strftime('%b %Y')
        if self.is_present:
            return f"{start} - Present"
        elif self.end_date:
            return f"{start} - {self.end_date.strftime('%b %Y')}"
        return start


class ContactMessage(models.Model):
    """Contact form messages"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
    
    def __str__(self):
        return f"{self.name} - {self.subject or 'No Subject'}"


class Service(models.Model):
    """Services offered"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="labb icon name")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title


class SiteSettings(models.Model):
    """Site-wide settings"""
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    
    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return self.key
    
    @classmethod
    def get_value(cls, key, default=''):
        try:
            return cls.objects.get(key=key).value
        except cls.DoesNotExist:
            return default
