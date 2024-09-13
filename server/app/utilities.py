from config import settings


def make_did(namespace, identifier):
    return f"did:web:{settings.DOMAIN}:{namespace}:{identifier}"


def data_key_from_did(namespace, identifier):
    return f"did:web:{settings.DOMAIN}:{namespace}:{identifier}"
