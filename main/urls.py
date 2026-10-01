from django.urls import path
from .views import (
    RegisterView,
    RestaurantListView,
    CategoryListView,
    FoodListView,
    OrderListCreateView,
    OrderItemCreateView,
)


urlpatterns = [
    
    path(
        'register/',
        RegisterView.as_view()
    ),

    path(
        'restaurants/',
        RestaurantListView.as_view()
    ),

    path(
        'categories/',
        CategoryListView.as_view()
    ),

    path(
        'foods/',
        FoodListView.as_view()
    ),

    path(
        'orders/',
        OrderListCreateView.as_view()
    ),

    path(
        'order-items/',
        OrderItemCreateView.as_view()
    ),
]