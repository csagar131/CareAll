from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User,CareSeeker,CareGiver

@receiver(post_save,sender = User)
def create_careseeker_giver(sender,created,instance,**kwargs):
    if created and instance.is_elder == True:
        care_seeker_obj = CareSeeker.objects.create(user = instance,funds = 0,is_available = True)
        care_seeker_obj.save()
    if created and instance.is_elder == False:
        care_giver_obj = CareGiver.objects.create(user = instance,earning = 0,active_care_count = 0)
        care_giver_obj.save()

    
       

