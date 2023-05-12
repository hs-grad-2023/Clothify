from django import template
from muapp.models import photos,viton_upload_cloth,viton_upload_model

register = template.Library()

@register.filter
def getGroupIdFirst(clothesgroupID): #c.groupID|getGroupId {{ somevariable|cut:"0" }}
    try:
        photosobject = photos.objects.filter(groupID=clothesgroupID).first().imgfile.url
        return photosobject #groupID와 일치하는 imgfile url을 리턴한다.

    except photos.DoesNotExist:
        return False

@register.filter
def getModelName(modelID): #c.groupID|getGroupId {{ somevariable|cut:"0" }}
    try:
        model_obj = viton_upload_model.objects.filter(ID__exact=modelID).first().clothesname
        model_obj = model_obj.split('.')[0]
        return model_obj #groupID와 일치하는 imgfile url을 리턴한다.

    except viton_upload_model.DoesNotExist:
        return False
    
@register.filter
def getClothName(clothID): #c.groupID|getGroupId {{ somevariable|cut:"0" }}
    try:
        cloth_obj = viton_upload_cloth.objects.filter(ID__exact=clothID).first().clothesname
        cloth_obj = cloth_obj.split('.')[0]

        return cloth_obj #groupID와 일치하는 imgfile url을 리턴한다.

    except viton_upload_cloth.DoesNotExist:
        return False

@register.filter
def delay(value, arg):
    return float(value) * float(arg)

@register.filter
def count_matching_comments(value, arg):
    return len([values for values in value if values.post_id == arg])

