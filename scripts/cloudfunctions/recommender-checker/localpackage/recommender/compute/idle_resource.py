import os
from google.cloud.asset_v1.types.assets import Asset
from proto.marshal.collections.repeated import RepeatedComposite
from typing import List
from ..recommender import Recommender


class InstanceIdleResourceRecommender(Recommender):
    def __init__(self):
        recommender_id = 'google.compute.instance.IdleResourceRecommender'
        asset_type = 'compute.googleapis.com/Instance'
        super().__init__(recommender_id, asset_type)

    def detect(self) -> None:
        project_identifiers_map = self._group_by_projects(self._list_assets())
        for project, properties in project_identifiers_map.items():
            print(f'check {project} recommendation')
            for zone in properties["zones"]:
                recommendations = self._list_recommendations(properties['project_number'], zone)
                if not recommendations:
                    continue
                for recommendation in recommendations:
                    payload = self._generate_slack_payload(project, recommendation)
                    self._post_slack_message(payload)

    def _list_assets(self) -> List[Asset]:
        asset_list = []
        page_token = ''
        while True:
            response = self.asset_client.list_assets(
                request={
                    "parent": f"organizations/{os.environ['ORGANIZATION_ID']}",
                    "asset_types": [self.asset_type],
                    "page_token": page_token
                }
            )
            asset_list += response.assets
            page_token = response.next_page_token
            if not page_token:
                break
        return asset_list

    def _list_recommendations(self, project_number: str, zone: str) -> RepeatedComposite:
        response = self.recommender_client.list_recommendations(
            request={
                "parent": f"projects/{project_number}/locations/{zone}/recommenders/{self.recommender_id}"
            }
        )
        return response.recommendations

    def _group_by_projects(self, assets: List[Asset]):
        """
        :return: {
          'project_name': {
            'project_number': '123456789000',
            'zones': ['asia-northeast1-a', 'asia-northeast1-c']
          }
        }
        """
        project_identifiers_map = {}
        for asset in assets:
            project_number = [a for a in asset.ancestors if 'projects/' in a][0].split('/')[1]
            project_name = asset.name.split('/projects/')[1].split('/')[0]
            zone = asset.name.split('/zones/')[1].split('/')[0]
            if project_name in project_identifiers_map:
                if zone not in project_identifiers_map[project_name]["zones"]:
                    project_identifiers_map[project_name]["zones"].append(zone)
            else:
                project_identifiers_map[project_name] = {
                    "project_number": project_number,
                    "zones": [zone]
                }
        return project_identifiers_map
