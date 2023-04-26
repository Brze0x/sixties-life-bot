import requests


def get_pln_news(category: str) -> dict:
    return requests.get(f'https://e0x.dev/sixtieslife/pln/{category}').json()

def get_cdi_news(category: str) -> dict:
    return requests.get(f'https://e0x.dev/sixtieslife/cdi/{category}').json()

def get_pg_news(category: str) -> dict:
    return requests.get(f'https://e0x.dev/sixtieslife/pg/{category}').json()

def get_ipsk_news(category: str) -> dict:
    return requests.get(f'https://e0x.dev/sixtieslife/ipsk/{category}').json()
