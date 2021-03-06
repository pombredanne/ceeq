from datetime import datetime, timedelta
import json
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from ceeq.apps.queries.models import Project, ScoreHistory
from ceeq.apps.users.views import user_is_superuser
from models import ProjectAccess


def update_project_access_history(request):
    """
    Update Project Access count per day
    :param request:
    :return:
    """
    projects = Project.objects.all()
    total_access = 0
    today = datetime.today().date()
    # today = (datetime.today() - timedelta(days=1)).date()

    for project in projects:
        score_history = project.scorehistory_set.all()
        for item in score_history:
            if item.access and item.created.date() == today:
                total_access += 1

    project_accesses = ProjectAccess.objects.all()
    for project_access in project_accesses:
        if project_access.created.date() == today:
            project_access.total = total_access
            project_access.save()
            break
    else:
        project_access = ProjectAccess.objects.create(total=total_access)


@login_required
def usage(request):
    if request.method == 'GET':
        return render(request, 'usage/usage.html')

    return HttpResponseNotFound()


def get_project_access_trend(request):
    project_accesses = ProjectAccess.objects.all().order_by('created')
    data = {}
    categories = []
    count = []

    for item in project_accesses:
        if item.created.month < 10:
            tmp_month = '0' + str(item.created.month)
        else:
            tmp_month = str(item.created.month)
        if item.created.day < 10:
            tmp_day = '0' + str(item.created.day)
        else:
            tmp_day = str(item.created.day)
        tmp_year = str(item.created.year)

        categories.append(tmp_year + '-' + tmp_month + '-' + tmp_day)

        tmp_list = []
        for sh in ScoreHistory.objects.filter(created__year=tmp_year,
                                              created__month=tmp_month,
                                              created__day=tmp_day,
                                              access=True):
            tmp_list.append(sh.project.name)

        count.append({
            'y': item.total,
            'extra': sorted(tmp_list)
        })

    data['categories'] = categories
    data['count'] = count

    return HttpResponse(json.dumps(data), content_type='application/json')


@user_passes_test(user_is_superuser)
def update_project_access_history_manually(request):
    update_project_access_history(request)

    return render(request, 'usage/usage.html')
