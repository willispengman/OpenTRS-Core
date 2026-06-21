from opentrs.metadata.model import RadiometricMetadata
from opentrs.metadata.parser import MetadataParser


def test_metadata_model_creation():
    metadata = RadiometricMetadata(
        emissivity=0.98,
        object_distance_m=2.0,
    )

    assert metadata.emissivity == 0.98
    assert metadata.object_distance_m == 2.0


def test_metadata_parser_returns_metadata():
    parser = MetadataParser(b"")

    metadata = parser.parse()

    assert isinstance(metadata, RadiometricMetadata)