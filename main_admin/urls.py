from django.urls import path

from main_admin.views import (
    main, remove, delete, add, add_category, new_product, add_new_product, auth, auth_page
)


urlpatterns = [
    path('', main, name='admin-main'),
    path('remove/<uuid:product_id>', remove, name='admin-remove-item'),
    path('delete/<uuid:product_id>', delete, name='admin-delete-item'),
    path('add/<uuid:product_id>', add, name='admin-add-item'),
    path('add_new_category', add_category, name='admin-add-category'),
    path('newProduct', new_product, name='admin-new-product'),
    path('add_new_product', add_new_product, name='admin-new-product'),
    
    path('auth', auth_page, name='admin-auth'),
    path('authorize', auth, name='admin-authorize'),
]