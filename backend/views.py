from django.http import HttpResponse


def error_500(request):
    return HttpResponse("Server Error")


def error_400(request, exception):
    return HttpResponse("Bad Request")


def error_403(request, exception):
    return HttpResponse("Permission Denied")


def error_404(request, exception):
    return HttpResponse("Not Found")
