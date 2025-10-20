from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    # Página inicial
    path('', views.home, name='home'),
    
    # Produtos
    path('produtos/', views.product_list, name='product_list'),
    path('categoria/<slug:slug>/', views.category_products, name='category_products'),
    path('produto/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # Autenticação
    path('cadastro/', views.register, name='register'),
    
    # Carrinho
    path('carrinho/', views.cart_detail, name='cart_detail'),
    path('adicionar-ao-carrinho/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('atualizar-carrinho/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('remover-do-carrinho/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # Checkout e Pedidos
    path('checkout/', views.checkout, name='checkout'),
    path('pedido/<str:order_number>/', views.order_detail, name='order_detail'),
    path('meus-pedidos/', views.order_history, name='order_history'),
]
