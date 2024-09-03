from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render
from rest_framework import viewsets, permissions

from .forms import UpdateProfileForm
from .models import Category
from .models import Image
from .serializers import CategorySerializer
from .serializers import ImageSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.filter(delete=False)
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        instance.delete = True
        instance.deleted_at = timezone.now()
        instance.save()


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})


def image_list(request, name):
    images = Image.objects.filter(category__name=name)
    return render(request, 'image_list.html', {'images': images})


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        terms = request.POST.get('terms')

        if not terms:
            messages.error(request, "You must agree to the terms and conditions.")
            return render(request, 'signup.html')

        if password != password_confirm:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('catigories')
        except:
            messages.error(request, "An error occurred. Please try again.")
            return render(request, 'signup.html')

    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('catigories')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'login.html')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        form = UpdateProfileForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': form})


@login_required
def delete_profile(request):
    user = request.user
    logout(request)
    user.delete()
    messages.success(request, "Your account has been deleted.")
    return redirect('signup')


def create_image(request):
    image = Image.objects.all()
    return render(request, 'create_image.html', {'images': images})


@login_required
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.save()
            return redirect('image_list')
    else:
        form = ImageUploadForm()
    return render(request, 'upload_image.html', {'form': form})


@login_required
def update_image(request, pk):
    image = get_object_or_404(Image, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            return redirect('image_list')
    else:
        form = ImageUploadForm(instance=image)
    return render(request, 'upload_image.html', {'form': form})


@login_required
def delete_image(request, pk):
    image = get_object_or_404(Image, pk=pk, user=request.user)
    if request.method == 'POST':
        image.delete()
        return redirect('image_list')
    return render(request, 'delete_image.html', {'image': image})
