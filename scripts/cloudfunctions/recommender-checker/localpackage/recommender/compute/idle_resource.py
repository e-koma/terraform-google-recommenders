import os
from google.cloud.asset_v1.types.assets import ResourceSearchResult
from proto.marshal.collections.repeated import RepeatedComposite
from typing import List
from ..recommender import Recommender


class VMIdleResourceRecommender(Recommender):
    def __init__(self):
        recommender_id = 'google.compute.instance.IdleResourceRecommender'
        asset_type = 'compute.googleapis.com/Instance'
        super().__init__(recommender_id, asset_type)

    def detect(self) -> None:
        assets_list = self._search_assets()
        for asset in assets_list:
            project_number = asset.project.split('/')[-1]
            project_name = asset.name.split('/projects/')[1].split('/')[0]
            print(f'check {project_name} {asset.display_name} compute instance idle recommendation')
            recommendations = self._list_recommendations(project_number, asset.location)
            if not recommendations:
                continue
            for recommendation in recommendations:
                payload = self._generate_slack_payload(project_name, recommendation)
                print(payload)
                self._post_slack_message(payload)

    def _search_assets(self) -> List[ResourceSearchResult]:
        asset_list = []
        page_token = ''
        while True:
            response = self.asset_client.search_all_resources(
                request={
                    "scope": f"organizations/{os.environ['ORGANIZATION_ID']}",
                    "asset_types": [self.asset_type],
                    "page_token": page_token
                }
            )
            asset_list += response.results
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
