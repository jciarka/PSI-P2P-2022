import json


class JsonSerializer:
    def __init__(self) -> None:
        pass

    def serialze(self, data_dict: dict) -> bytes:
        json_str = json.dumps(data_dict)
        return bytes(json_str, 'utf-8')

    def deserialzie(self, json_bytes: bytes) -> dict:
        try:
            json_str = json_bytes.decode('utf-8')
            return json.loads(json_str)
        except json.JSONDecodeError:
            return None
