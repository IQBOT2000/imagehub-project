from app.views import category_list, image_list
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from app.views import signup, login_view, logout_view

from app.views import profile_view, update_profile, delete_profile

from app.views import upload_image, delete_image, update_image

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('app.urls')),
    path('categories/', category_list, name='category_list'),
    path('categories/<str:name>/', image_list, name='image_list'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/update/', update_profile, name='update_profile'),
    path('profile/delete/', delete_profile, name='delete_profile'),
    path('images/upload/', upload_image, name='upload_image'),
    path('images/<int:pk>/edit/', update_image, name='update_image'),
    path('images/<int:pk>/delete/', delete_image, name='delete_image'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
