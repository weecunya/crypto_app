from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .forms import RegisterForm
from .models import CryptoPrice


# Create your views here.
@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, 'registration/register.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'registration/register.html', {'form': form})

@csrf_exempt
@login_required
def profile(request):
    return render(request, 'registration/profile.html')

@require_http_methods(['GET'])
@csrf_exempt
def crypto_history(request):
    symbol = request.GET.get('symbol')
    print(symbol)
    prices = CryptoPrice.objects.filter(symbol=symbol).order_by('-timestamp')[:50]
    return render(request,'history.html', {'prices':prices,'symbol': symbol})

@require_http_methods(['GET'])
@csrf_exempt
def api_btc_history(request):
    symbol = request.GET.get('symbol')
    result = CryptoPrice.objects.filter(symbol=symbol).order_by('-timestamp')[:50]
    result = list(reversed(result))
    prices = [float(p.price) for p in result]
    labels = [p.timestamp.strftime('%H:%m') for p in result]
    return JsonResponse({'prices': prices, 'labels': labels})

@require_http_methods(['GET'])
@csrf_exempt
def chart(request):
    symbol = request.GET.get('symbol')
    return render(request, 'crypto_chart.html', {'symbol': symbol})