import os
from localpackage.recommender.compute.idle_resource import VMIdleResourceRecommender
from localpackage.recommender.cloudsql.idle_resource import CloudSQLIdleResourceRecommender

def check_recommender(_event, context):
    print(f'This Function was triggered by messageId {context.event_id} published at {context.timestamp}')

    if os.environ['IDLE_VM_RECOMMENDER_ENABLED'] == 'true':
        idle_vm_recommender = VMIdleResourceRecommender()
        idle_vm_recommender.detect()
    if os.environ['IDLE_SQL_RECOMMENDER_ENABLED'] == 'true':
        idle_sql_recommender = CloudSQLIdleResourceRecommender()
        idle_sql_recommender.detect()
