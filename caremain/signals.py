from django.db.models.signals import post_save
from django.dispatch import receiver
from caremain.models import CareRequests,Transaction
from accounts.models import CareGiver,CareSeeker

@receiver(post_save,sender=Transaction)
def complete_service(sender,created,instance,**kwargs):
    if created:
        caregiver = CareGiver.objects.get(user = instance.caregiver)
        careseeker = CareSeeker.objects.get(user = instance.careseeker)
        careseeker.set_is_available_true()
        careseeker.deduct_fund(instance.tamount)
        careseeker.save()
        caregiver.decrement_care_count()
        caregiver.add_earning(instance.tamount)
        caregiver.save()


        


