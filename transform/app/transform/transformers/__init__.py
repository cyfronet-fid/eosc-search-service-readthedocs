# pylint: disable=undefined-variable, cyclic-import
"""Import transformations"""
from app.settings import settings

from .bundle import BundleTransformer
from .catalogue import CatalogueTransformer
from .data_source import DataSourceTransformer
from .dataset import DatasetTransformer
from .guideline import transform_guidelines
from .offer import OfferTransformer
from .organisation import OrganisationTransformer
from .other_rp import OtherRPTransformer
from .project import ProjectTransformer
from .provider import ProviderTransformer
from .publication import PublicationTransformer
from .service import ServiceTransformer
from .software import SoftwareTransformer
from .training import TrainingTransformer

__all__ = ["transformers"]

transformers = {
    settings.SERVICE: ServiceTransformer,
    settings.DATASOURCE: DataSourceTransformer,
    settings.PROVIDER: ProviderTransformer,
    settings.OFFER: OfferTransformer,
    settings.BUNDLE: BundleTransformer,
    settings.GUIDELINE: transform_guidelines,
    settings.TRAINING: TrainingTransformer,
    settings.OTHER_RP: OtherRPTransformer,
    settings.SOFTWARE: SoftwareTransformer,
    settings.DATASET: DatasetTransformer,
    settings.PUBLICATION: PublicationTransformer,
    settings.ORGANISATION: OrganisationTransformer,
    settings.PROJECT: ProjectTransformer,
    settings.CATALOGUE: CatalogueTransformer,
}
