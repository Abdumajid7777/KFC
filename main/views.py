
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from .permissions import IsReviewOwnerOrReadOnly, IsRestaurantOwnerOrReadOnly
from django.contrib.auth.models import User
from rest_framework import generics, viewsets
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Restaurant,Category,Food,Order,OrderItem, Review
from .serializers import UserSerializer,RestaurantSerializer,CategorySerializer, ReviewSerializer, FoodSerializer,OrderSerializer,OrderItemSerializer, LoginSerializer, RegisterSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.exceptions import PermissionDenied

class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsRestaurantOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'category': ['exact'],
        'price': ['gte', 'lte'],
    }

    def perform_create(self, serializer):
        # Ресторан эгаси фақат ўз ресторанига блюдо қўша олишини таъминлаш
        restaurant = getattr(self.request.user, 'restaurant', None)
        if not restaurant:
            raise PermissionDenied("Сизда ресторан мавжуд эмас ёки сиз ресторан эгаси эмассиз.")
        serializer.save(restaurant=restaurant)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsReviewOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class RestaurantListView(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class FoodListView(generics.ListAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

    filterset_fields = {
        'category': ['exact'],
        'price': ['gte', 'lte'],
    }


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        ).prefetch_related('items')

    def perform_create(self, serializer):
        serializer.save()


class OrderItemCreateView(generics.CreateAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(
            order__user=self.request.user
        )

    def perform_create(self, serializer):
        order = serializer.validated_data['order']

        if order.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(
                'Вы не можете добавлять товары в чужой заказ.'
            )

        serializer.save()

@api_view(['POST'])
def logout(request):
    
    if request.user.is_authenticated:
        Token.objects.filter(
            user=request.user
        ).delete()
        return Response({
            'message': "Logout successful"
        })
    return Response({
        'message': ' не был авторизован'
    })


@api_view(['POST'])
def login(request):
  
    serializer = LoginSerializer(
        data=request.data
    )
    if serializer.is_valid():
        user = serializer.validated_data['user']

        token, created = Token.objects.get_or_create(
            user = user
        )
        return Response({
            'messages': "Login successful",
            'token': token.key
        })
    return Response(
        serializer.errors,
        status=400
    )



@api_view(['POST'])
def register(request):

    serializer = RegisterSerializer(
        data=request.data
    )
    if serializer.is_valid():
        user = serializer.save()

        return Response(
            {
                "Answer": "Successful",
                'username': user.username
            },
            status = status.HTTP_201_CREATED
        )
    return Response(
        serializer.errors,
        status = status.HTTP_400_BAD_REQUEST
    )