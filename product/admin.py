from django.contrib import admin

from product.models import Category, Product, SubCategory


admin.site.empty_value_display = 'Не задано'


class CategoryInline(admin.StackedInline):
    model = Category
    extra = 0


class SubCategoryInline(admin.StackedInline):
    model = SubCategory
    extra = 0


class ProductInline(admin.StackedInline):
    model = Product
    extra = 0


class CategoryAdminInline(admin.ModelAdmin):
    inlines = (CategoryInline,)
    list_display = (
        'name',
        'slug',
        'image',
        'subcategoreies',
    )
    search_fields = ('name', 'slug',)
    list_display_links = ('name',)


class SubCategoryAdmin(admin.ModelAdmin):
    inlines = (ProductInline,)
    list_display = (
        'name',
        'slug',
        'image',
        'price',
        'subcategoreies'
    )
    search_fields = ('name', 'slug',)
    list_display_links = ('name',)


class ProductAdmin(admin.ModelAdmin):
    inlines = (SubCategoryInline,)
    list_display = (
        'name',
        'slug',
        'image',
    )
    search_fields = ('name', 'slug',)
    list_display_links = ('name',)


admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
