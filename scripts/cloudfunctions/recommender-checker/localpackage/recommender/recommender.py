import json
import os
from google.cloud import asset_v1
from google.cloud import recommender_v1
from google.cloud.recommender_v1.types.recommendation import Recommendation
from typing import TypedDict
from urllib.request import Request, urlopen


class Recommender():
    SlackPayload = TypedDict('SlackPayload', {'text': str})

    def __init__(self, recommender_id, asset_type, ignore_descriptions=['']):
        # AssetTypes: https://cloud.google.com/asset-inventory/docs/supported-asset-types
        # RecommenderId: https://cloud.google.com/recommender/docs/recommenders
        self.recommender_client = recommender_v1.RecommenderClient()
        self.recommender_id = recommender_id
        self.asset_client = asset_v1.AssetServiceClient()
        self.asset_type = asset_type
        self.ignore_descriptions = ignore_descriptions

    def _list_assets(self):
        raise NotImplementedError

    def _list_recommendations(self):
        raise NotImplementedError

    def _generate_slack_payload(self, project: str, recommendation: Recommendation) -> SlackPayload:
        _id = self.recommender_id.strip('google.')
        message = f"[GCP] {project}の推奨事項 ({_id})\n" \
                  f"```" \
                  f"RecommendType: {recommendation.recommender_subtype}\n" \
                  f"Description: {recommendation.description}\n" \
                  f"```"
        payload = {'text': message}
        return payload

    def _post_slack_message(self, payload: SlackPayload) -> None:
        slack_hook_url = os.environ.get('SLACK_HOOK_URL')
        if slack_hook_url is None:
            print(payload)
            return
        req = Request(slack_hook_url, json.dumps(payload).encode("UTF-8"))
        with urlopen(req) as response:
            response.read()
            print("Message posted to Slack")
