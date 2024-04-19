from django.http import HttpResponse
from django.shortcuts import redirect,render
from django.urls import reverse_lazy
from .forms import SignUpForm,DepositeForm,ProfileForm
from django.views.generic import CreateView,View,FormView
from django.contrib import messages
from django.contrib.auth import logout,login
from django.contrib.auth.views import LoginView,PasswordChangeView
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from books.models import Borrow
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
# Create your views here.
def send_email(user, subject,amount, template):
        message = render_to_string(template, {
            'user' : user,
            'subject':subject,
            'amount':amount
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()


class Login(LoginView):
    template_name = 'login_form.html'
    def form_valid(self, form):
        messages.success(self.request,'Logged in Successful')
        return super().form_valid(form)
    def get_success_url(self) -> str:
        send_email(self.request.user,'Logined In','','LoginMail.html')
        return reverse_lazy('home')
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class SignUp(FormView):
    form_class = SignUpForm
    template_name = 'signup_form.html'
    success_url = reverse_lazy('user_login')
    def form_valid(self, form):
        user=form.save()
        login(self.request,user)
        messages.success(self.request,'Signed Up Successful')
        send_email(self.request.user,'Signed Up','','LoginMail.html')
        return super().form_valid(form)
    
@method_decorator(login_required,name='dispatch')
class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('user_login')

@method_decorator(login_required,name='dispatch')
class Profile(LoginRequiredMixin, View):
    template_name = 'profile.html'
    
    def get(self, request):
        form = ProfileForm(instance=request.user)
        borrows = Borrow.objects.filter(borrower=request.user)
        context = {'form': form, 'borrows': borrows}
        return render(request, self.template_name, context)

    def post(self, request):
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile') 
        borrows = Borrow.objects.filter(borrower=request.user)
        context = {'form': form, 'borrows': borrows}
        return render(request, self.template_name, context)
    
@method_decorator(login_required,name='dispatch')
class ChangePassword(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'pass_change_form.html'
    success_url = reverse_lazy('profile')
    def form_valid(self, form):
        messages.success(self.request,'Password Updated Successfully')
        return super().form_valid(form)

class DepositeView(LoginRequiredMixin,View):
    form_class = DepositeForm
    template_name = 'deposite.html'
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account = request.user.account
            account.balance += amount
            account.save(update_fields=['balance'])
            messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
            )
            send_email(self.request.user,'Deposite Money Request',amount,'DepositeMail.html')
            return redirect('home')
        return render(request, self.template_name, {'form': form})

