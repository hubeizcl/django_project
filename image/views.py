from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Image
from .form import ImageForm


# Create your views here.

@login_required('/account/login/')
@csrf_exempt
@require_POST
def upload_image(request):
    form = ImageForm(data=request.POST)
    if form.is_valid():
        try:
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            return HttpResponse({'status': "1"})
        except:
            return JsonResponse({'status': "0"})


@login_required("/account/login/")
def list_image(request):
    images = Image.objects.filter(user=request.user)
    return render(request, 'image/list_images.html', {"images": images})
