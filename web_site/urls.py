from app.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/categories/', permanent=False)),
    path('admin/', admin.site.urls),
    path('api/', include('app.urls')),

    # Категории и изображения
    path('categories/', category_list, name='category_list'),
    path('categories/<str:name>/', image_list, name='image_list'),
    path('categories/<str:name>/upload/', upload_image, name='upload_image'),
    path('categories/<str:name>/<int:id>/', image_detail, name='image_detail'),

    # Профиль пользователя
    path('profile/', profile_view, name='profile'),
    path('profile/update/', update_profile, name='update_profile'),
    path('profile/delete/', delete_profile, name='delete_profile'),

    # Аутентификация
    path('signup/', signup, name='signup'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # "Мои изображения"
    path('my-images/', my_images, name='my_images'),
    path('my-images/update/<int:image_id>/', update_image, name='update_image'),
    path('my-images/delete/<int:image_id>/', delete_image, name='delete_image'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
