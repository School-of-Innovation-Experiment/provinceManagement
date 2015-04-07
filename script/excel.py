# coding: UTF-8
from school.utility import *

project_list = get_current_project_query_set().filter(project_recommend_status__status = RECOMMEND_SECOND_ROUND_PASSED)
print project_list.count()
