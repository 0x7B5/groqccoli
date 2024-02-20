import random
import requests
import time
import json
from .models import Chat, Stats


class Client:
    def __init__(self, proxies=None, user_agent=None, retries=0):
        self._proxies = proxies
        self._user_agent_path = "user_agents.txt"

        self._user_agent = self._get_user_agent() if user_agent is None else user_agent
        self._auth_token = self._get_anon_token()

        self._retries = retries
        self._headers = {
            "Host": "api.groq.com",
            "Connection": "keep-alive",
            "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            "sec-ch-ua-mobile": "?0",
            "User-Agent": self._user_agent,
            "Accept": "*/*",
            "Origin": "https://groq.com",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://groq.com/",
            "Accept-Language": "en-US,en;q=0.9",
        }
        self._auth_token_last_updated = int(time.time())
        self._API_URL = "https://api.groq.com/v1/request_manager/text_completion"

    def create_chat(
        self,
        user_prompt,
        model_id="mixtral-8x7b-32768",
        system_prompt="Please try to provide useful, helpful and actionable answers.",
        history=[],
        seed=10,
        max_tokens=32768,
        temperature=0.2,
        top_k=40,
        top_p=0.8,
        max_input_tokens=21845,
    ) -> Chat:
        json_data = {
            "model_id": model_id,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "history": history,
            "seed": seed,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p,
            "max_input_tokens": max_input_tokens,
        }

        response = requests.post(
            self._API_URL,
            headers=self._headers,
            json=json_data,
            stream=True,
        )

        res = ""
        request_id = None
        stats = Stats(
            time_generated=0, tokens_generated=0, time_processed=0, tokens_processed=0
        )

        for chunk in response.iter_lines(decode_unicode=True):
            if chunk:  # filter out keep-alive new chunks
                try:
                    loaded = json.loads(chunk)

                    if loaded["result"].get("requestId", None):
                        request_id = loaded["result"]["requestId"]

                    if loaded["result"].get("stats", None):
                        stats = Stats(
                            time_generated=loaded["result"]["stats"]["timeGenerated"],
                            tokens_generated=loaded["result"]["stats"][
                                "tokensGenerated"
                            ],
                            time_processed=loaded["result"]["stats"]["timeProcessed"],
                            tokens_processed=loaded["result"]["stats"][
                                "tokensProcessed"
                            ],
                        )

                    res += loaded["result"].get("content", "")
                    # print(loaded["result"].get("content", ""), end="")
                    # print(loaded["result"].get("stats", ""), end="")
                except Exception as e:
                    pass

        return Chat(
            content=res,
            request_id=request_id,
            stats=stats,
        )

    def _get_anon_token(self):
        response = requests.get(
            "https://api.groq.com/v1/auth/anon_token",
            headers=self._headers,
            proxies=self._proxies,
        )
        return response.json()["access_token"]

    def _get_user_agent(self):
        with open(self._user_agent_path, "r") as file:
            return random.choice(file.readlines()).strip()
