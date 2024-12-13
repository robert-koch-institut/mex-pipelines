from pydantic import BaseModel


class ZenodoCreatorsOrContributors(BaseModel):
    """Model subclass for Zenodo metadata Creators or Contributors."""

    name: str | None = None


class ZenodoRelateditdentifiers(BaseModel):
    """Model subclass for Zenodo metadata related identifiers."""

    identifier: str | None = None
    relation: str | None = None


class ZenodoLicense(BaseModel):
    """Model subclass for Zenodo metadata license."""

    id: str | None = None


class ZenodoFiles(BaseModel):
    """Model subclass for Zenodo file id."""

    id: str | None = None


class ZenodoMetadata(BaseModel):
    """Model subclass for Zenodo metadata dict."""

    title: str | None = None
    description: str | None = None
    creators: list[ZenodoCreatorsOrContributors] = []
    contributors: list[ZenodoCreatorsOrContributors] = []
    keywords: list[str] = []
    related_identifiers: list[ZenodoRelateditdentifiers] = []
    language: str | None = None
    license: ZenodoLicense


class ZenodoParentRecordSource(BaseModel):
    """Model class for a Zenodo record as resource parent."""

    conceptrecid: str | None = None
    modified: str | None = None
    id: int | None = None
    conceptdoi: str | None = None
    metadata: ZenodoMetadata


class ZenodoRecordVersion(BaseModel):
    """Model class for Versions of a record."""

    created: str | None = None
    doi_url: str | None = None
    id: int | None = None
    metadata: ZenodoMetadata
    files: list[ZenodoFiles]
    modified: str | None = None
    conceptrecid: str | None = None
