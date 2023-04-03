from django import template
from muapp.models import clothes, photos

register = template.Library()

@register.filter
def getGroupIdFirst(clothesgroupID): #c.groupID|getGroupId {{ somevariable|cut:"0" }}
    photosobject = photos.objects.filter(groupID=clothesgroupID).first().imgfile.url

    return photosobject #groupID와 일치하는 imgfile url을 리턴한다.
