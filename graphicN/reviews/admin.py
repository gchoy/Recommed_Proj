from django.contrib import admin

from .models import Comic, Review, Cluster

class ReviewAdmin(admin.ModelAdmin):
   model = Review
   list_display = ('comic', 'rating', 'user_name', 'comment', 'pub_date')
   list_filter = ['pub_date', 'user_name']
   search_fields = ['comment']

class ClusterAdmin(admin.ModelAdmin):
    model = Cluster
    list_display = ['name', 'get_members']

admin.site.register(Comic)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Cluster, ClusterAdmin)
