import json
import base64

from .jsn import pre_json_dump


def obj_to_base64(d: dict) -> str:
    """Turns your pure Python dict/thing into a base64 encoded JSON blob."""
    return (
        base64.b64encode(json.dumps(pre_json_dump(d)).encode()).decode()
        if d
        else ""
    )


def base64_to_obj(b64next: str) -> dict:
    """Takes a b64 encoded JSON object and turns it back into whatever your code originally provided."""
    return (
        json.loads(base64.b64decode(b64next.encode()).decode())
        if b64next
        else {}
    )
