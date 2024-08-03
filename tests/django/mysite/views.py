from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def view_zero_division(request):
    1 / 0
