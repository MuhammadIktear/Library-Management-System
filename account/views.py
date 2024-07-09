from django.shortcuts import render
from django.views.generic import FormView
from .forms import UserRegisterForm,editUserForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,LogoutView
from django.views import View
from django.shortcuts import redirect
from library.models import Order
class UserRegistrationView(FormView):
    # accounts/user_registration.html
    template_name = 'accounts/user_register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('user_login')
    
    def form_valid(self,form):
        print(form.cleaned_data)
        user = form.save()
        login(self.request, user)
        print(user)
        return super().form_valid(form)
    
class UserLoginView(LoginView):
    # accounts/user_login.html
    template_name = 'accounts/user_login.html'
    def get_success_url(self):
        return reverse_lazy('home')

class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return redirect(reverse_lazy('home'))  
    
@login_required
def user_profile(request):
    if request.method == 'POST':
        form = editUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
    else:
        form = editUserForm(instance=request.user)
    orders = Order.objects.filter(user=request.user)  # Adjust the field according to your model
    
    return render(request, 'accounts/profile.html', {'form': form, 'orders': orders})
