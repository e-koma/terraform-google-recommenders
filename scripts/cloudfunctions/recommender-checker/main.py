import os
from localpackage.recommender.compute.idle_resource import InstanceIdleResourceRecommender


def check_recommender(_event, context):
    print(f'This Function was triggered by messageId {context.event_id} published at {context.timestamp}')

    if os.environ['IDLE_VM_RECOMMENDER_ENABLED'] == 'true':
        instance_idle_recommender = InstanceIdleResourceRecommender()
        instance_idle_recommender.detect()
