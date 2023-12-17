from trackerapp.models import CourseInfo, DoseInfo
from django.utils.timezone import localtime

def notif_context_data(request):
    qs_id = CourseInfo.objects.filter(user=request.user).values('id')
    datetoday = localtime()
    notif = DoseInfo.objects.filter(courseinfo_id__in=qs_id).filter(
        dose_timing__year=datetoday.year,
        dose_timing__month=datetoday.month,
        dose_timing__day=datetoday.day
        ).select_related() #for notif
    notif_count = len(notif)
    
    return {'notif': notif, 'notif_count': notif_count, 'datetoday': datetoday}