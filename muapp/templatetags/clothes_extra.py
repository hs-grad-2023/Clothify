from django import template
from muapp.models import photos

register = template.Library()

@register.filter
def getGroupIdFirst(clothesgroupID): #c.groupID|getGroupId {{ somevariable|cut:"0" }}
    try:
        photosobject = photos.objects.filter(groupID=clothesgroupID).first().imgfile.url
        return photosobject #groupID와 일치하는 imgfile url을 리턴한다.

    except photos.DoesNotExist:
        return False

@register.filter
def delay(value, arg):
    return float(value) * float(arg)

