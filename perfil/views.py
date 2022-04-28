from django.urls import reverse
from decimal import Decimal
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from perfil.models import AffiliateApplication, Plan, PlanPago, Profile
from perfil.forms import AffiliateApplicationForm, PagarPlanForm
from perfil import enzona
from django.shortcuts import redirect, render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class HomeView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'inicio.html'
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['bienvenido']="HOLA INICIO"
        return context

def initPerfil(request):
    try:
        profile = Profile.objects.create(usuario=request.user)
        messages.success(request, "Perfil de usuario registrado")
    except:
        pass
    return HttpResponseRedirect('/')




#*************************************************************
def pagarPlan(request):
    context={}
   
    if request.method=="POST":
        # form = PagarPlanForm(request.POST)
        # if not form.is_valid():
        print("Form VALIDO")
        # print(form)
        # form.save(commit=False)
        # name = request.cleaned_data.get("title")
        # description = form.cleaned_data.get("description")
        # price = form.cleaned_data.get("price")
        name = request.POST.get("title")
        description = request.POST.get("description")
        price = request.POST.get("price")
        plan_type = request.POST.get("plan_type")
        plan = request.POST.get("plan")
    
        # new_format_price = "{0:.2f}".format(price / 100)
        new_format_price = f"{price}"
        
        

        items = []
        temp_item = {
        'name': name, #OJO ---> Los nombres no pueden tener caracteres especiales porque da error
        'description': description,
        'quantity': 1,
        'price': new_format_price,
        'tax': '0.00'
        }
        items.append(temp_item)
    
        amount = {
            "total": new_format_price,
            "details": {
            "shipping": "0.00",
            "tax": "0.00",
            "discount": "0.00",
            "tip": "0.00"
            }
        }
        
    
            
###################### BLOQUE DE CONSULTA A ENZONA #######################
        resp_enzona = enzona.post_payments(
            description=description,
            currency="CUP",
            amount=amount,
            items=items,
            cancel_url=f'http://{request.get_host()}/', #OK
            return_url=f'http://{request.get_host()}/confirmar-pago/' #OK
            )
        print("resp_enzona.json()")
        print(resp_enzona.json())
        if resp_enzona.status_code == 200:
            
            resp_content = resp_enzona.json()
            links_resp = resp_content['links']
            url_confirm = links_resp[0]
            context['url_confirm'] = url_confirm
            request.session["pago_plan"]=request.user.pk
            request.session["plan_type"]=plan_type
            request.session["plan"]=plan
            request.session["amount"]=resp_content['amount']['total']

            
            # guardar valores en session para desdupes de confirmado el pago utilizarlos y eliminarlos
            return redirect(to=url_confirm['href']) #Redirecciona a enzona para confirmar el pago
        else:
            print("resp_enzona.status_code")
            print(resp_enzona.status_code)
            print(resp_enzona.status_code)
                
        
            context['resp_enzona'] = resp_enzona.json()
    return HttpResponse('Pagado')

#*********************************************************************************************






class PlanesView(LoginRequiredMixin, generic.TemplateView):
    template_name='planes.html'

    def get_context_data(self, **kwargs):
        context = super(PlanesView, self).get_context_data(**kwargs)
        context['planes']=Plan.objects.all()
        return context





class ConfirmarPagoView(LoginRequiredMixin, generic.View): #Confirma el pago realizado por el usuario
    def get(self, request, *args, **kwargs):
        pago_plan=None
        try:
        
            plan_type=request.session["plan_type"]
            plan=request.session["plan"]
            pago_plan = request.session['pago_plan']
            amount = request.session['amount']
            print("pago_plan")
            print(pago_plan)
            print("pago_plan")
            print(plan)
            print("plan_type")
            print(plan_type)
        except:
            pass
        transaction_uuid = request.GET['transaction_uuid']
        user_uuid = request.GET['user_uuid']
        profile=Profile.objects.get(usuario=request.user)
        plan =Plan.objects.get(pk=1)
      
        #*******************************************************
        # Logica para agregar el producto digital a la libreria#
        #*******************************************************
        pago_plan = PlanPago.objects.create(
            plan_type=plan_type,
            plan=plan,
            profile=profile,
            amount=amount,
            purchused=True,
            transaction_uuid=transaction_uuid,
            user_uuid=user_uuid,
            credit=plan.credit,
        )
        profile.presupuesto+=Decimal(float(amount))
        profile.save()
        # user_library = UserLibrary.objects.get(user=request.user)
        # product = Product.objects.get(id=digital_product)
        # user_library.products.add(product)
        # user_library.save()
        del request.session["plan_type"]
        del request.session["plan"]
        del request.session["amount"]
        del request.session['pago_plan']
        # del request.session['digital_product']
        try: 
            ref_profile = request.session['ref_profile'] #Recibir referencia y agregarla a la cuenta del usuario
            profile = Profile.objects.get(id=ref_profile)
            profile.recommended_digital_products.add(product)
            profile.save() 
            del request.session['ref_profile'] #Elimina la referencia de usuario
        except:
            pass

        messages.info(request, message=f"Se ha realizado correctamente el pago ahora usted tiene un credigo de {amount} cup")
        # UserLibrary
        



        confirm = enzona.confirm_payment_orders(transaction_uuid)
        print("confirm")
        print(confirm)
        return redirect(to="perfil:gracias")


class GraciasView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'gracias.html'
    def get_context_data(self, **kwargs):
        context = super(GraciasView,self).get_context_data(**kwargs)
        # messages.info(self.request, message="Se ha realizado Correctamente el pago y el producto se ha agregado a su libreria de descargas")

        return context
    

                

class PagarPlanView(LoginRequiredMixin, generic.TemplateView):

    template_name = 'shop/confirm_enzona_payment.html'
    def post(self, request, *args, **kwargs):
        if request.method=="POST":
            form = PaymentDigitalProductForm(request.POST)
            print(form)
            if form.is_valid():
                name = form.cleaned_data.get("title")
                description = form.cleaned_data.get("description")
                price = form.cleaned_data.get("price")
            
                new_format_price = "{0:.2f}".format(price / 100)
                context = super(EnzonaPaymentDigitalProductView, self).get_context_data(**kwargs)
                
        
                items = []
                temp_item = {
                'name': name, #OJO ---> Los nombres no pueden tener caracteres especiales porque da error
                'description': description,
                'quantity': 1,
                'price': new_format_price,
                'tax': '0.00'
                }
                items.append(temp_item)
         
                amount = {
                    "total": new_format_price,
                    "details": {
                    "shipping": "0.00",
                    "tax": "0.00",
                    "discount": "0.00",
                    "tip": "0.00"
                    }
                }
             
         
                request.session["digital_product"]=kwargs['pk']
            
 ###################### BLOQUE DE CONSULTA A ENZONA #######################
                resp_enzona = enzona.post_payments(
                    description="description",
                    currency="CUP",
                    amount=amount,
                    items=items,
                    cancel_url=f'http://{request.get_host()}/shop/', #OK
                    return_url=f'http://{request.get_host()}/shop/confirm-order/' #OK
                    )
                print("resp_enzona.json()")
                print(resp_enzona.json())
                if resp_enzona.status_code == 200:
                   
                    resp_content = resp_enzona.json()
                    links_resp = resp_content['links']
                    url_confirm = links_resp[0]
                    context['url_confirm'] = url_confirm
                    # guardar valores en session para desdupes de confirmado el pago utilizarlos y eliminarlos
                    return redirect(to=url_confirm['href']) #Redirecciona a enzona para confirmar el pago
                else:
                    print("resp_enzona.status_code")
                    print(resp_enzona.status_code)
                    print(resp_enzona.status_code)
                    
            
                context['resp_enzona'] = resp_enzona.json()

 ###################### FIN BLOQUE DE CONSULTA A ENZONA #######################

        # order.payment_method='ENZONA'
        # order.save()
        context['order'] = get_or_set_order_session(self.request)
        # print('=====================================')
        # print(order.items.all())
        # print('=====================================')
    

        # context['CALLBACK_URL']= self.request.build_absolute_uri(reverse("shop:thank-you"))
        return context




def affiliateApplication(request):
    profile = Profile.objects.get(usuario=request.user)
    if profile.phone and profile.ci:
        form = AffiliateApplicationForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            afi = AffiliateApplication.objects.get(profile=profile)
            if afi and afi.aprovated == True:
                profile.affiliated=True
                profile.save()
                messages.success(request, "Su cuenta de afiliado ha sido restablecida")
                return HttpResponseRedirect('/')
            elif afi and afi.aprovated == False:
                afi.aprovated = True
                afi.save()
                messages.success(request, "Se ha reactivado su cuenta de afiliado")
                return HttpResponseRedirect('/')
            if not afi:
                AffiliateApplication.objects.create(profile=profile, aprovated=True)
                profile.affiliated=True
                profile.save()
            
                messages.info(request, "Su cuenta de afiliado ha sido creada")
                return HttpResponseRedirect('/')
        else:
            messages.info(request, "Error al enviar la solicitud, por favor revisar los requisitos")
            return HttpResponseRedirect('/')
    else:
        messages.error(request, "Antes de solicitar la cuenta de afilidado, debe editar su perfil y agregar su numero de telefono y CI")
        return HttpResponseRedirect(reverse('perfil:editar-perfil', kwargs={'pk':profile.pk}))




def referedCode(request, *args, **kwargs):

	code = str(kwargs.get('ref_code'))
	next_url = str(request.GET.get('next_url'))

	try:
		profile = Profile.objects.get(code=code)
		
		request.session['ref_profile']=profile.id

	except:
		pass
	
	url = request.build_absolute_uri()
	# print("URL REFER")
	print(next_url)
	return HttpResponseRedirect(next_url)


class EditarPerfilView(generic.UpdateView):
    model=Profile
    fields = ['profile_info','phone','ci','gender','picture','first_name','last_name']
    template_name='user/editar_perfil.html'

class DetallePerfilView(generic.DetailView):
    # model=Profile
    queryset=Profile.objects.all()
    
    template_name='user/detalle_perfil.html'
	#****************************************************************************************************
	# La funcion establece que si el usuario no es el propietario da error 404 (no encuentra la pagina) #
	#****************************************************************************************************

    def get_queryset(self):
         queryset = super(DetallePerfilView, self).get_queryset()
         return queryset.filter(usuario=self.request.user)

class ListaPagosView(generic.ListView):
    queryset=PlanPago.objects.all()
    template_name='user/lista_de_pagos.html'

    def get_queryset(self):
         queryset = super(ListaPagosView, self).get_queryset()
         return queryset.filter(profile=self.request.user.profile)

class DetallesPagoView(generic.DetailView):
    template_name='user/detalles_pago.html'
    queryset=PlanPago.objects.all()

    def get_queryset(self):
         queryset = super(DetallesPagoView, self).get_queryset()
         return queryset.filter(profile=self.request.user.profile)
