from config import settings

ISSUERS: dict = {
    "director-of-petroleum-lands": {
        "id": f"did:web:{settings.DOMAIN}:petroleum-and-natural-gas-act:director-of-petroleum-lands",
        "name": "Director of Petroleum Lands",
        "description": "An officer or employee of the ministry who is designated as the Director of Petroleum Lands by the minister.",
    },
    "chief-permitting-officer": {
        "id": f"did:web:{settings.DOMAIN}:mines-act:chief-permitting-officer",
        "name": "Chief Permitting Officer",
        "description": "The person designated under section 8.2 as the chief permitting officer.",
    },
}
VERIFICATION_METHODS: dict = {
    "director-of-petroleum-lands": [
        {
            'id': f'did:web:{settings.DOMAIN}:petroleum-and-natural-gas-act:director-of-petroleum-lands#key-01', 
            'type': 'MultiKey', 
            'controller': f'did:web:{settings.DOMAIN}:petroleum-and-natural-gas-act:director-of-petroleum-lands', 
            'publicKeyMultibase': 'z6Mkw5XFPNprFbxL27ZCThN6MQFULih94PSqYMECT3MEgMLE'
        },
        {
            'id': f'did:web:{settings.DOMAIN}:petroleum-and-natural-gas-act:director-of-petroleum-lands#key-02', 
            'type': 'JsonWebKey', 
            'controller': f'did:web:{settings.DOMAIN}:petroleum-and-natural-gas-act:director-of-petroleum-lands', 
            'publicKeyJwk': {
                "kty":"OKP",
                "crv":"Ed25519",
                "x":"9wUXJ9V3_t2uybuOjhO_m0ESyFyYGdbl7UqSTtRKJBM"
            }
        },
    ],
    "chief-permitting-officer": [
        {
            'id': f'did:web:{settings.DOMAIN}:mines-act:chief-permitting-officer#key-01', 
            'type': 'MultiKey', 
            'controller': f'did:web:{settings.DOMAIN}:mines-act:chief-permitting-officer', 
            'publicKeyMultibase': 'z6MkhaE81srJobCo6y8JFKkxJgBa7kFhnBM5QSos8sgJr2ny'
        },
        {
            'id': f'did:web:{settings.DOMAIN}:mines-act:chief-permitting-officer#key-02', 
            'type': 'JsonWebKey', 
            'controller': f'did:web:{settings.DOMAIN}:mines-act:chief-permitting-officer', 
            'publicKeyJwk': {
                "kty":"OKP",
                "crv":"Ed25519",
                "x":"Llvzh_8cjEIYh3C5foM4uunBrywjfgTTbrhFPSN_fqY"
            }
        }
    ],
}
SERVICES: dict = {
    "director-of-petroleum-lands": [{
        "id": f"did:web:{settings.DOMAIN}:petroleum-and-natural-gas-act:director-of-petroleum-lands#ministry",
        "type": "LinkedDomain",
        "serviceEndpoint": "https://www2.gov.bc.ca/gov/content/industry/natural-gas-oil/petroleum-natural-gas-tenure",
    }],
    "chief-permitting-officer": [{
        "id": f"did:web:{settings.DOMAIN}:mines-act:chief-permitting-officer#ministry",
        "type": "LinkedDomain",
        "serviceEndpoint": "https://www2.gov.bc.ca/gov/content/industry/mineral-exploration-mining/permitting",
    }],
}
CREDENTIAL_TYPES: list = [
    "PetroleumAndNaturalGasTitle",
    "MinesActPermit",
]
CREDENTIALS: dict = {
    "0eb53970-9e0d-4965-922e-5179ff24657b": {
        "issuer": "director-of-petroleum-lands",
        "type": "PetroleumAndNaturalGasTitle",
        "entityId": "A0131571",
        "format": "vc-di",
    },
    "762651c9-6f4c-472d-a88c-ab3f7653a3d6": {
        "issuer": "director-of-petroleum-lands",
        "type": "PetroleumAndNaturalGasTitle",
        "entityId": "A0131571",
        "format": "vc-jwt",
    },
    # 'a0024292-3f8e-4543-a8f7-f4dda199006f': {},
    # 'fda7802f-6629-4722-8047-2dca4c7745e3': {},
    # '762651c9-6f4c-472d-a88c-ab3f7653a3d6': {},
}
