import json
from fastapi import HTTPException
from aries_askar import Store
from app.plugins.agent import AgentController
from app.models import DidDocument, VerificationMethod
from config import settings
from app.data import ISSUERS, CREDENTIAL_TYPES, CREDENTIALS, VERIFICATION_METHODS, SERVICES
import hashlib
import json
import time
import hashlib


class AskarStorage:
    def __init__(self):
        self.db = settings.ASKAR_DB
        self.key = Store.generate_raw_key(
            hashlib.md5(settings.DOMAIN.encode()).hexdigest()
        )

    async def provision(self, recreate=True):
        await Store.provision(self.db, "raw", self.key, recreate=recreate)
        time.sleep(5)
        for issuer in ISSUERS:
            seed = hashlib.md5(f'{settings.SECRET_KEY}:{issuer}'.encode()).hexdigest()
            AgentController().register_did(ISSUERS[issuer]["id"], seed=seed)
            did_doc = DidDocument(
                id=ISSUERS[issuer]["id"],
                authentication=[ISSUERS[issuer]["id"]+'#key-01'],
                assertionMethod=[ISSUERS[issuer]["id"]+'#key-01'],
                verificationMethod=VERIFICATION_METHODS[issuer],
                service=SERVICES[issuer],
            ).model_dump()
            await self.store("did", ISSUERS[issuer]["id"], did_doc)

        for credential_type in CREDENTIAL_TYPES:
            with open(f"app/data/contexts/{credential_type}.jsonld", "r") as f:
                await self.store(
                    "context", f"{credential_type}:v0", json.loads(f.read())
                )

        for credential_id in CREDENTIALS:
            credential_type = CREDENTIALS[credential_id]["type"]
            entity_id = CREDENTIALS[credential_id]["entityId"]
            issuer = CREDENTIALS[credential_id]["issuer"]
            with open(f"app/data/credentials/{credential_id}.jsonld", "r") as f:
                credential = json.loads(f.read())

            credential["@context"].append(
                f"https://{settings.DOMAIN}/contexts/{credential_type}/v0"
            )
            credential["id"] = (
                f"https://{settings.DOMAIN}/entities/{entity_id}/credentials/{credential_id}"
            )
            credential["issuer"] = ISSUERS[CREDENTIALS[credential_id]["issuer"]]
            
            if CREDENTIALS[credential_id]["format"] == 'vc-di':
                options = AgentController().issuer_proof_options(ISSUERS[issuer]["id"]+'#key-01')
                vc = AgentController().issuer_vc_di(credential, options)
                
            elif CREDENTIALS[credential_id]["format"] == 'vc-jwt':
                options = AgentController().issuer_proof_options(ISSUERS[issuer]["id"]+'#key-02')
                vc = AgentController().issuer_vc_jwt(credential, options)

            await self.store("credential", f'{entity_id}:{credential_id}', vc)

    async def open(self):
        return await Store.open(self.db, "raw", self.key)

    async def fetch(self, category, data_key):
        store = await self.open()
        try:
            async with store.session() as session:
                data = await session.fetch(category, data_key)
            return json.loads(data.value)
        except:
            return None

    async def store(self, category, data_key, data):
        store = await self.open()
        try:
            async with store.session() as session:
                await session.insert(
                    category,
                    data_key,
                    json.dumps(data),
                    {"~plaintag": "a", "enctag": "b"},
                )
        except:
            raise HTTPException(status_code=400, detail="Couldn't store record.")
