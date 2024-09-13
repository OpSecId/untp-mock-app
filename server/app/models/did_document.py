from typing import Union, List, Dict, Any
from pydantic import BaseModel, Field, AliasChoices, field_validator

CONTEXT = [
    "https://www.w3.org/ns/did/v1", 
    "https://w3id.org/security/jwk/v1",
    "https://w3id.org/security/multikey/v1",
]


class BaseModel(BaseModel):
    def model_dump(self, **kwargs) -> Dict[str, Any]:
        return super().model_dump(by_alias=True, exclude_none=True, **kwargs)


class VerificationMethod(BaseModel):
    id: str = Field()
    type: str = Field()
    controller: str = Field()
    publicKeyMultibase: str = Field()


class Service(BaseModel):
    id: str = Field()
    type: str = Field()
    serviceEndpoint: str = Field()


class DidDocument(BaseModel):
    context: List[str] = Field(CONTEXT, alias="@context")
    id: str = Field()
    controller: str = Field(None)
    authentication: List[str] = Field()
    assertionMethod: List[str] = Field()
    verificationMethod: List[dict] = Field()
    service: List[dict] = Field(None)
