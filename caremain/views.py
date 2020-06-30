from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import View
from accounts.models import CareGiver,User,CareSeeker
from django.views.generic import DetailView,ListView,UpdateView
from django.http import HttpResponse
from caremain.models import CareRequests,Transaction,Review
from caremain.forms import StartServiceForm,ReviewForm
from accounts.views import AddFundView
from accounts.forms import AddFundForm
from datetime import datetime,timedelta

class IndexView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'index.html')


class ListElders(View):
    def get(self,request,*agrs,**kwargs):
        if request.user.is_elder == False:
            elders = User.objects.filter(is_elder = True).exclude(username = 'admin')
            return render(request,'listcandidate.html',context = {'elders':elders})


class CandidateDetailView(View):  
    def get(self,request,slug,*args,**kwargs):
        usr = User.objects.get(slug = slug)
        context = {'usr':usr}
        if CareRequests.objects.filter(caregiver = self.request.user,careseeker = usr,status = 'pending').exists():
            context['req_status'] = 'pending'
        if self.request.user.is_elder == False:
            context['careseeker'] = CareSeeker.objects.get(user = usr)
        reviews = Review.objects.filter(review_for = usr)
        context['reviews'] = reviews
        context['form'] = ReviewForm()
        return render(request,'detailuser.html',context)

    def post(self,request,slug,*args,**kwargs):
        form = ReviewForm(request.POST)
        form.is_valid()
        print(form.cleaned_data)
        review_for = User.objects.get(slug=slug)
        Review.objects.create(review_for = review_for ,review_by=request.user,\
        comment = form.cleaned_data['review'],rating = form.cleaned_data['rating'])
        return redirect('candidatedetail',slug = slug)


class SendCareRequestView(View):
    def get(self,request,slug,*args,**kwargs):
        caregiver = CareGiver.objects.get(user = request.user)
        careseeker = User.objects.get(slug = slug)
        if CareRequests.objects.filter(careseeker = careseeker,caregiver = request.user,status = 'rejected').exists():
            return HttpResponse("Your previous request has been rejected you can't send another request")
        if caregiver.get_active_care_count() < 4:
            carerequest = CareRequests.objects.create(caregiver = request.user,\
            careseeker = careseeker,status = 'pending')
            carerequest.save()
        else:
            return HttpResponse("you have exceeded the care taking limit")
        if CareRequests.objects.filter(caregiver = request.user,careseeker = careseeker,status = 'pending').exists():
            current_req_status = 'pending'
        careseekeruser = CareSeeker.objects.get(user = careseeker)
        return render(request,'detailuser.html',\
        context={'usr':careseeker,'careseeker': careseekeruser,'req_status':current_req_status})


class AcceptRejectRequestView(View):  #this wiil be the view where several conditions will be checked
    def get(self,request,str,slug,*args,**kwargs):
        care_seeker = CareSeeker.objects.get(user = request.user)
        giver = User.objects.get(slug = slug)
        care_giver = CareGiver.objects.get(user = giver)
        care_request = CareRequests.objects.get(careseeker = request.user,caregiver = giver)
        if str == 'approve':
            if CareRequests.objects.filter(careseeker = request.user,status = 'approved'):
                return HttpResponse("You have already approved one Request")
            if CareRequests.objects.filter(careseeker = request.user,status = 'active'):
                return HttpResponse("You have already one member there to be cared")
            care_seeker.set_is_available_false()
            care_seeker.save()
            care_giver.increment_care_count()
            care_giver.save()
            care_request.status = 'approved'
            care_request.save()
        if str == 'reject':
            care_request.status = 'rejected'
            care_request.save()
        active_request = CareRequests.objects.filter(careseeker = request.user).filter(status ='active')
        approved_request = CareRequests.objects.filter(careseeker = request.user).filter(status ='approved')
        req_statuses = CareRequests.objects.filter(careseeker = request.user).filter(status ='pending')
        return render(request,'dashboard.html',context={'req_statuses':req_statuses,\
        'active':active_request,'approve':approved_request})


class StartServiceView(View):
    def get(self,request,slug,*args,**kwargs):
        form = StartServiceForm()
        usr = User.objects.get(slug = slug)
        caregiver = CareGiver.objects.get(user = usr)
        context = {'form':form,'caregiver':caregiver}
        return render(request,'startserviceform.html',context)

    def post(self,request,slug,*args,**kwargs):
        form = StartServiceForm(request.POST)
        form.is_valid()
        usr = User.objects.get(slug = slug) #caregiver main user object
        caregiver = CareGiver.objects.get(user = usr)
        charges_per_month = caregiver.rate_per_month
        chagers_per_day = charges_per_month/30
        total_bill = form.cleaned_data['days'] * chagers_per_day
        careseeker = CareSeeker.objects.get(user = request.user)
        if careseeker.funds < total_bill:
            return redirect(reverse('addfund',kwargs = {'slug':slug}))
        else:
            care_request = CareRequests.objects.filter(caregiver = usr,careseeker = request.user) 
            care_request.update(start_service = datetime.now(),status = 'active', \
            end_service = datetime.now() +timedelta(days=form.cleaned_data['days']))
            return redirect('dashboard')


class EndServiceView(View):
    def get(self,request,slug,*args,**kwargs):
        caregiver_user_obj = User.objects.get(slug = slug)
        caregiver = CareGiver.objects.get(user = caregiver_user_obj)
        careseeker_user_obj = User.objects.get(id = request.user.id)
        careseeker = CareSeeker.objects.get(user = request.user)
        carerequest = CareRequests.objects.get(careseeker =careseeker_user_obj,caregiver = caregiver_user_obj)
        bill_amount = self.calculate_transaction_amount(caregiver_user_obj,caregiver,careseeker_user_obj,careseeker,carerequest)
        transaction = Transaction.objects.create(careseeker=careseeker_user_obj,caregiver = caregiver_user_obj,tamount = bill_amount)
        transaction.save()
        carerequest.set_request_status('completed')
        carerequest.save()
        return redirect('dashboard')

    def calculate_transaction_amount(self,caregiver_user_obj,caregiver,careseeker_user_obj,careseeker,carerequest):
        charges_per_month = caregiver.rate_per_month
        chagers_per_day = charges_per_month/30
        start_date = carerequest.start_service.replace(tzinfo=None)
        end_date = datetime.now().replace(tzinfo=None)
        print(start_date)
        print(end_date)
        days_till_now = (end_date - start_date).days
        bill_amount = days_till_now * chagers_per_day
        return bill_amount



























