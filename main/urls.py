from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FoodViewSet,
    ReviewViewSet,
    RegisterView,
    RestaurantListView,
    CategoryListView,
    FoodListView,
    OrderListCreateView,
    OrderItemCreateView,
    logout,
    login,
)

router = DefaultRouter()
router.register(r'food-viewsets', FoodViewSet)
router.register(r'review-viewsets', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('register/', RegisterView.as_view(), name='register'),
    path('restaurants/', RestaurantListView.as_view(), name='restaurant-list'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('foods/', FoodListView.as_view(), name='food-list'),
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('order-items/', OrderItemCreateView.as_view(), name='order-item-create'),
    path('logout/', logout, name='logout'),
    path('login/', login, name='login'),
]