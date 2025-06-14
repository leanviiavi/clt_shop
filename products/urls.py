from django.urls import path

from products.views import (
    # products_page, create_category, create_subcategory, current_product, to_cart, my_cart,
    # product_remove, product_add, product_delete, bye_cart
    GetProductsAPI, GetImageAPI, CategoryesAPI, SubcategoryesAPI, ProductsActionsAPI, CartAPI, FiltersAPI,
    AdminAuthAPI, StatisticAPI,
)


urlpatterns = [
    # path('', products_page, name='products'),
    # path('<uuid:product_id>', current_product, name='current_product'),
    # path('toCart/<uuid:product_id>', to_cart, name='to_cart'),
    # path('createCategory', create_category, name='create_category'),
    # path('createSubcategory', create_subcategory, name='create_subcategory'),

    # path('myCart', my_cart, name='my_cart'),
    # path('remove/<uuid:product_id>', product_remove, name='product_remove'),
    # path('delete/<uuid:product_id>', product_delete, name='product_delete'),
    # path('add/<uuid:product_id>', product_add, name='product_add'),
    # path('bye', bye_cart, name='bye_cart')

    path('products', GetProductsAPI.as_view(), name='get-create-products'),
    path('image/', GetImageAPI.as_view(), name='get-image'),
    path('categoryes/', CategoryesAPI.as_view(), name='get-create-categoryes'),
    path('subcategoryes', SubcategoryesAPI.as_view(), name='get-create-subcategoryes'),
    path('productActions/', ProductsActionsAPI.as_view(), name='update-products-count'),
    path('carts', CartAPI.as_view(), name='get-create-carts'),
    path('filters/', FiltersAPI.as_view(), name='get-filters'),
    path('admin/auth', AdminAuthAPI.as_view(), name='admin-auth'),
    path('statistic', StatisticAPI.as_view(), name='admin-statistic'),
]