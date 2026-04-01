from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if dictionary:
        return dictionary.get(key)
    return None

@register.filter(name='has_group')
def  has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()