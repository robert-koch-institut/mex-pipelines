from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)

from mex.common.identity.registry import register_provider
from mex.extractors.pipeline import load_job_definitions
from mex.identity import BackendIdentityProvider
from mex.types import ExtractorIdentityProvider

defs = load_job_definitions()
register_provider(ExtractorIdentityProvider.BACKEND, BackendIdentityProvider)
