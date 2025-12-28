import enum


class APIResources(enum.Enum):
    project = "projects"
    group = "groups"

    @classmethod
    def from_entity_type(cls, entity_type: str) -> "APIResources":
        if entity_type not in cls.__members__:
            raise ValueError(f"Unknown entity type: {entity_type}")
        return cls[entity_type]


class Files(enum.Enum):
    manual_default_config = "config.yaml"
