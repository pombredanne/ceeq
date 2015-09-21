from django.shortcuts import get_object_or_404
from ceeq import celery_app

from ceeq.apps.calculator.models import ImpactMap, ComponentImpact, ComponentComplexity, ResultHistory, SeverityMap
from ceeq.apps.calculator.utils import get_table_data, get_score_data, get_score_by_component
from ceeq.apps.queries.models import Project


@celery_app.task
def calculate_score(project_id):
    project = get_object_or_404(Project, pk=project_id)
    result_latest = project.resulthistory_set.latest('confirmed')
    query_results = result_latest.query_results

    internal_table = get_table_data(query_results, 'internal')
    uat_table = get_table_data(query_results, 'uat')
    combined_table = get_table_data(query_results, 'overall')

    internal_score = get_score_data(query_results, 'internal')
    uat_score = get_score_data(query_results, 'uat')
    overall_score = get_score_data(query_results, 'overall')

    # score_by_component = get_score_by_component(query_results, 'overall')

