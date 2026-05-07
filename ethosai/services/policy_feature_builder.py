from typing import Dict

from services.features.permission_features import (
    build_permission_features
)

from services.features.price_features import (
    build_price_features
)

from services.features.similarity_features import (
    build_similarity_features
)


def build_all_features(
    metadata: Dict,
    robots_data: Dict,
    tos_data: Dict
) -> Dict:

    permission_features = (
        build_permission_features(
            metadata,
            robots_data,
            tos_data
        )
    )

    price_features = (
        build_price_features(
            metadata,
            robots_data,
            tos_data
        )
    )

    similarity_features = (
        build_similarity_features(
            metadata,
            robots_data,
            tos_data
        )
    )

    return {

        "permission_features":
            permission_features,

        "price_features":
            price_features,

        "similarity_features":
            similarity_features
    }