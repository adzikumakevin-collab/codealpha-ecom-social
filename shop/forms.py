import re
from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Ex: Jean'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Ex: Dupont'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ex: jean@email.com'}),
            'address': forms.TextInput(attrs={'placeholder': 'Ex: 12 Rue des Sports'}),
            'postal_code': forms.TextInput(attrs={'placeholder': 'Ex: 75001'}),
            'city': forms.TextInput(attrs={'placeholder': 'Ex: Paris'}),
        }

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code')
        
        # Dictionnaire de regex pour différents pays
        # France: 5 chiffres (ex: 75001)
        # USA: 5 chiffres suivis optionnellement d'un tiret et 4 chiffres (ex: 90210-1234)
        # UK: Format complexe alphanumérique (ex: SW1A 1AA)
        formats = {
            'FR': r'^\d{5}$',
            'US': r'^\d{5}(-\d{4})?$',
            'UK': r'^[A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2}$'
        }

        # Ici, on teste par exemple par rapport au format français par défaut
        # Pour bien faire, il faudrait un champ "pays" dans votre formulaire pour choisir la regex
        if not re.match(formats['FR'], postal_code):
            raise forms.ValidationError("Le format du code postal est invalide pour la France (5 chiffres attendus).")
            
        return postal_code