from affiliate.forms import ShortenerForm
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from affiliate.models import Shortener
from django.shortcuts import render

# Create your views here.


def affiliateLinks(request):
    context ={
        'links':Shortener.objects.filter(user=request.user)
    }
    return render(request, template_name='affiliate/links.html',context=context)




def shortener(request):
    #Debo agregar el refercode + la url del producto
    user = request.user
   
    if request.method=="POST":
        form = ShortenerForm(request.POST)
        if form.is_valid():
            shortener = form.save(commit=False)
            long_url = request.POST.get('long_url')
            product_id = request.POST.get('product_id')
            product = Product.objects.get(id=product_id)
   
            new_long_url = f'profile-user/ref-code/{user.profile.code}/?next_url={long_url}'
    
            shortener.long_url = new_long_url
            shortener.user = user
            shortener.product = product
            shortener.save()
            return HttpResponseRedirect(reverse('affiliate:links'))
        else:
            form = ShortenerForm()
    else:
        form=ShortenerForm()



def redirect_url_view(request, shortened_part):

    try:
        shortener = Shortener.objects.get(short_url=shortened_part)

        shortener.times_followed += 1        

        shortener.save()
        # new_url = request.build_absolute_uri('/') + shortened_object.short_url
        print("request.get_host('/')")
        print(request.build_absolute_uri('/'))
        print(request.get_host())
        next_url = request.build_absolute_uri('/') + shortener.long_url
        print(next_url)
        
        return HttpResponseRedirect(next_url)
        
    except:
        raise Http404('Lo sentimos, enlace roto :(')