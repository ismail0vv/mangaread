from django.contrib import admin
from manga.models import Genre, Type, Manga

# Register your models here.


class MangaAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'genres_list',
                    'release_year', 'description']
    search_fields = ['title', 'type', 'release_year']
    list_filter = ['type', 'genres']
    list_editable = ['release_year']
    list_per_page = 100
    prepopulated_fields = {"slug": ("title",)}

    def genres_list(self, obj):
        return '\n'.join(g.name for g in obj.genres.all())


admin.site.register(Genre)
admin.site.register(Type)
admin.site.register(Manga, MangaAdmin)
