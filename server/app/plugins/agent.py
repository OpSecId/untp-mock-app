from fastapi import HTTPException
from config import settings
from datetime import datetime, timezone, timedelta
import requests
import secrets


class AgentController:
    def __init__(self):
        self.endpoint = settings.AGENT_ENDPOINT

    def register_did(self, did, seed=None):
        # TODO remove this section once seed is optional in acapy
        if not seed:
            seed = secrets.token_hex(16)
        r = requests.post(
            f"{self.endpoint}/did/web",
            json={
                "id": f"{did}#key-01",
                "key_type": "ed25519",
                "seed": seed,
                "type": "MultiKey",
            },
        )
        try:
            return r.json()["verificationMethod"]
        except:
            raise HTTPException(
                status_code=r.status_code, detail="Couldn't create did."
            )

    def issuer_proof_options(self, verification_method):
        return {
            "type": "DataIntegrityProof",
            "cryptosuite": "eddsa-jcs-2022",
            "proofPurpose": "assertionMethod",
            "verificationMethod": verification_method,
            "created": str(datetime.now(timezone.utc).isoformat("T", "seconds")),
        }

    def issuer_vc_di(self, document, options):
        r = requests.post(
            f"{self.endpoint}/wallet/di/add-proof",
            json={"document": document, "options": options},
        )
        try:
            return r.json()["securedDocument"]
        except:
            raise HTTPException(
                status_code=r.status_code, detail="Couldn't sign document."
            )

    def issuer_vc_jwt(self, document, options):
        r = requests.post(
            f"{self.endpoint}/wallet/jwt/sign",
            json={
                'did': document['issuer']['id'],
                'headers': {},
                'payload': document,
                'verificationMethod': options['verificationMethod']
            },
        )
        try:
            return {
                "@context": ["https://www.w3.org/ns/credentials/v2"],
                "type": ["EnvelopedVerifiableCredential"],
                "id": f"data:application/vc-ld+jwt,{r.json()}"
            }
        except:
            raise HTTPException(
                status_code=r.status_code, detail="Couldn't sign document."
            )
