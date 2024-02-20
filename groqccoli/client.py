import random
import requests
import time
import json
from .models import Chat, Stats
from .constants import USER_AGENTS
from contextlib import contextmanager


class StreamingChat:
    def __init__(self, url, headers, json_data):
        self._url = url
        self._headers = headers
        self._json_data = json_data
        self._response = None

    def __enter__(self):
        self._response = requests.post(
            self._url, headers=self._headers, json=self._json_data, stream=True
        )

        def iterator():
            for chunk in self._response.iter_lines(decode_unicode=True):
                if chunk:
                    try:
                        loaded = json.loads(chunk)
                        yield loaded["result"].get("content", "")
                    except Exception as e:
                        pass

        return iterator()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._response:
            self._response.close()


class Client:
    def __init__(self, proxies=None, user_agent=None, retries=0):
        self._proxies = proxies
        self._user_agent = (
            random.choice(USER_AGENTS) if user_agent is None else user_agent
        )
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
        self._auth_token = self._get_anon_token()
        self._headers["authorization"] = "Bearer " + self._auth_token

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
        if model_id == "llama2-70b-4096":
            max_tokens = min(4096, max_tokens)
            max_input_tokens = min(2730, max_input_tokens)

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
                except Exception as e:
                    pass

        return Chat(
            content=res,
            request_id=request_id,
            stats=stats,
        )

    def create_streaming_chat(
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
    ):
        if model_id == "llama2-70b-4096":
            max_tokens = min(4096, max_tokens)
            max_input_tokens = min(2730, max_input_tokens)

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

        return StreamingChat(self._API_URL, self._headers, json_data)

    def _get_anon_token(self):
        response = requests.get(
            "https://api.groq.com/v1/auth/anon_token",
            headers=self._headers,
            proxies=self._proxies,
        )
        return response.json()["access_token"]
