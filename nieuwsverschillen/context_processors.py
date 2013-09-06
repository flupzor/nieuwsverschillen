from nieuwsverschillen.models import Source

def source_list(request):
    return { 'source_list': Source.objects.all() }
