from django import template

register = template.Library()

from ..models import Projects, SubProjects

# @register.inclusion_tag('clock.html')
# def get_sub_projects():
#     subprojects = SubProjects.objects.all()
#     return  {'subprojects':subprojects}

@register.inclusion_tag('subprojects.html', takes_context=True)
def show_subprojects(context, project):
    #project_id = project_list
    
    choices = SubProjects.objects.all()
    
    return {'choices':choices}