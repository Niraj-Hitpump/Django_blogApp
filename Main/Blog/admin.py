from django.contrib import admin
from django.db.models.signals import post_migrate
from taggit.models import Tag
from .models import BlogModel

class BlogModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_approved')  # Show title, user, and approval status
    list_filter = ('is_approved', 'user')  # Enable filtering
    search_fields = ('title', 'content', 'tags__name')  # Enable search for title, content, and tags

    def save_model(self, request, obj, form, change):
        if request.user.is_staff:
            obj.is_approved = True  # Automatically approve blogs created by admins
        obj.save()  # Save the object

# Function to create predefined tags after migration
def create_predefined_tags(sender, **kwargs):
    predefined_tags = ["classic"]
    for tag in predefined_tags:
        Tag.objects.get_or_create(name=tag)  # Create the tag if it doesn't exist

# Connect the post_migrate signal to the create_predefined_tags function
post_migrate.connect(create_predefined_tags, dispatch_uid="create_predefined_tags")

admin.site.register(BlogModel, BlogModelAdmin)
