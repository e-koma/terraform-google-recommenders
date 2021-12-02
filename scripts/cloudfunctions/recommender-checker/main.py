import os
from localpackage.recommender.compute.idle_resource import InstanceIdleResourceRecommender
# from localpackage.recommender.resourcemanager.project_utilization import ProjectUtilizationRecommender


def check_recommender(_event, context):
    print(f'This Function was triggered by messageId {context.event_id} published at {context.timestamp}')

    if os.environ['IDLE_VM_RECOMMENDER_ENABLED'] == 'true':
        instance_idle_recommender = InstanceIdleResourceRecommender()
        instance_idle_recommender.detect()
    # if os.environ['IDLE_PROJECT_RECOMMENDER_ENABLED'] == 'true':
    #     project_utilization_recommender = ProjectUtilizationRecommender()
    #     project_utilization_recommender.detect()
