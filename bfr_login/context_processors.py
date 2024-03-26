from category_management.models import Category


def nav(request):
    catt=Category.objects.all()
    return {'catt': catt}