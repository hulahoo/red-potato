from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from cart.views import CartViewSet
from main.views import ProductViewSet, CommentViewSet

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'cart', CartViewSet, basename='CartView')

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    # add this line
    # path('payments/', include('payments.urls')),
    path('account/', include('account.urls')),
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
