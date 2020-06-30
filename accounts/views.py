from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView,UpdateView
from accounts.models import User,CareSeeker,CareGiver
from django.views import View
from accounts.forms import ElderSignupForm,YoungerSignupForm,EditProfileForm,AddFundForm
from caremain.forms import ReviewForm
from caremain.models import CareRequests
from django.http import HttpResponse


class ElderUserCreate(CreateView):
    form_class = ElderSignupForm
    template_name = 'signup_elder.html'
    success_url = '/accounts/login'

    

class YoungerUserCreate(CreateView):
    form_class = YoungerSignupForm
    template_name = 'signup_younger.html'
    success_url = '/accounts/login'


class DisplayProfileView(View):
    def get(self,request,slug,*args,**kwargs):
        form = ReviewForm()
        if request.user.is_elder == True:
            careseeker= CareSeeker.objects.get(user = request.user) 
            return render(request,'profile.html',context = {'careseeker':careseeker,'form':form})
        return render(request,'profile.html',context = {'form':form})

class EditProfileView(UpdateView):
    model = User
    template_name = 'editprofile.html'
    form_class = EditProfileForm
    success_url = 'profile'

    def get_success_url(self,*args,**kwargs):
        return reverse('profile', kwargs={'slug': self.object.slug})


class UserDashboardView(View):
    def get(self,request,*args,**kwargs):
        if request.user.is_elder == False:
            req_statuses = CareRequests.objects.filter(caregiver = request.user)
            return render(request,'dashboard.html',context={'req_statuses':req_statuses})
        
        if request.user.is_elder == True:
            active_request = CareRequests.objects.filter(careseeker = request.user).filter(status ='active')
            approved_request = CareRequests.objects.filter(careseeker = request.user).filter(status ='approved')
            req_statuses = CareRequests.objects.filter(careseeker = request.user,status ='pending').order_by('-timestamp')
            context={'req_statuses':req_statuses,'active':active_request,'approve':approved_request}
            return render(request,'dashboard.html',context)


class AddFundView(View):
    def get(self,request,*args,**kwargs):
        form = AddFundForm()
        curr_amount = CareSeeker.objects.get(user = request.user).get_funds()
        return render(request,'addfund.html',context={'form':form,'amount':curr_amount})

    def post(self,request,*args,**kwargs):
        form = AddFundForm(request.POST)
        form.is_valid()
        careseeker =  CareSeeker.objects.get(user = request.user)
        amount = form.cleaned_data['fund']
        careseeker.allocate_fund(amount)  #calling the allocate_fund method of careseeker object
        careseeker.save()
        return render(request,'profile.html',context={'careseeker':careseeker})
        

