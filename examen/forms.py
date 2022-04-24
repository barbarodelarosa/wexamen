from django import forms
from .models import Examen, Pregunta, Respuesta, PreguntasRespondidas

class ElegirInlineFormset(forms.BaseInlineFormSet):
    def clean(self):
        super(ElegirInlineFormset, self).clean()

        respuesta_correcta = 0
        for formulario in self.forms:
            if not formulario.is_valid():
                return
            if formulario.cleaned_data and formulario.cleaned_data.get('correcta') is True:
                respuesta_correcta += 1

        try:
            assert respuesta_correcta == Pregunta.NUMERO_DE_RESPUESTAS_PERMITIDAS
        except AssertionError:
            raise forms.ValidationError("Una sola respuesta es permitida")




class CrearExamenForm(forms.ModelForm):
    
    # category = forms.ModelMultipleChoiceField(label="Categorias", queryset=Category.objects.all(), required=False)
    # merchant = forms.ModelChoiceField(queryset = Merchant.objects.none(),label="Tienda", widget=Select(attrs={'class':'select2'}), required=False)
    # brand = forms.ModelChoiceField(queryset = Brand.objects.none(), label="Marca", widget=Select(attrs={'class':'select2'}), required=False)
    # # tag = forms.ModelMultipleChoiceField(label="Etiquetas", queryset=Tag.objects.all(),widget=Select(attrs={'class':'select2', 'multiple':'multiple'}), required=False)
    # product_images = forms.FileField(label="Galeria del producto",help_text="Agregar hasta 5 imagenes del producto", widget=forms.ClearableFileInput(attrs={'multiple': True}), required=True)
    # # avialable_colours = forms.ModelMultipleChoiceField(label="Colores", queryset=ColorVariation.objects.none(),widget=Select(attrs={'class':'select2', 'multiple':'multiple'}), required=False)
    # # avialable_sizes = forms.ModelMultipleChoiceField(label="Medidas", queryset=SizeVariation.objects.none(),widget=Select(attrs={'class':'select2', 'multiple':'multiple'}), required=False)
    # # related_products = forms.ModelMultipleChoiceField(label="Productos relacionados", queryset=Product.objects.none(),widget=Select(attrs={'class':'select2', 'multiple':'multiple'}), required=False)
    # title=forms.CharField(label="Nombre del producto", help_text="Agregar nombre descriptivo del producto")
    # image=forms.ImageField(label="Imagen principal", help_text="Poner la imagen principal del producto")
    # price=forms.IntegerField(label="Precio", help_text="Agregar precio del producto")
    # stock=forms.IntegerField(label="Productos en stock", help_text="Agregar la cantidad de productos disponibles para la venta")
    # old_price=forms.IntegerField(label="Precio anterior", help_text="Solo agregar si existe un precio anterior menor al actual")
    # description=forms.Textarea()
    # details=RichTextField()
    # for_auction=forms.BooleanField(label="Producto para subasta", required=False, initial=False)

    class Meta:
        model = Examen
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user')
    #     super().__init__(*args, **kwargs)
        
        
        # # self.fields['category'].queryset = Category.objects.all()
        # self.fields['merchant'].queryset = Merchant.objects.filter(user=user)
        # self.fields['brand'].queryset = Brand.objects.all()
        # # self.fields['tag'].queryset = Tag.objects.all()
        # self.fields['product_images'].queryset = ProductImagesContent.objects.filter(user=user)
        # # self.fields['avialable_colours'].initial = ColorVariation.objects.all()
        # # self.fields['avialable_sizes'].initial = SizeVariation.objects.all()
     
        