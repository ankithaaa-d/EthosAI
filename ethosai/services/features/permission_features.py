import os
import torch
import logging

from transformers import (
    AutoTokenizer,
    AutoModel
)

from torch import nn

# ── Logging ─────────────────────────────────────────────
logger = logging.getLogger(__name__)

# ── Model Config ────────────────────────────────────────
MODEL_NAME = (
    "sentence-transformers/all-MiniLM-L6-v2"
)

MODEL_PATH = os.getenv(
    "PERMISSION_MODEL_PATH",
    "models/permission_model.pt"
)

LABELS = [
    "allowed",
    "conditional",
    "restricted"
]

# ── Tokenizer ───────────────────────────────────────────
tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

# ── Model Architecture ─────────────────────────────────
class PermissionClassifier(nn.Module):

    def __init__(self):

        super().__init__()

        self.encoder = (
            AutoModel.from_pretrained(
                MODEL_NAME
            )
        )

        self.fc = nn.Linear(
            384,
            len(LABELS)
        )

    def forward(
        self,
        input_ids,
        attention_mask
    ):

        outputs = self.encoder(

            input_ids=input_ids,

            attention_mask=attention_mask
        )

        cls = outputs.last_hidden_state[:, 0]

        return self.fc(cls)

# ── Lazy-loaded model ───────────────────────────────────
_model = None


def get_model():

    global _model

    if _model is None:

        logger.info(
            "Loading permission model..."
        )

        _model = PermissionClassifier()

        _model.load_state_dict(

            torch.load(
                MODEL_PATH,
                map_location="cpu"
            )
        )

        _model.eval()

    return _model


# ── Text builder ────────────────────────────────────────
def build_text(
    features: dict
):

    return " ".join([

        str(features.get(
            "domain",
            ""
        )),

        str(features.get(
            "content_type",
            ""
        )),

        str(features.get(
            "has_robots_txt",
            ""
        )),

        str(features.get(
            "robots_allows_ai",
            ""
        )),

        str(features.get(
            "robots_raw",
            ""
        )),

        str(features.get(
            "tos_exists",
            ""
        )),

        str(features.get(
            "tos_text_excerpt",
            ""
        )),

        str(features.get(
            "requires_license",
            ""
        )),

        str(features.get(
            "has_paywall",
            ""
        ))
    ])


# ── Main inference API ──────────────────────────────────
def predict_permission(
    features: dict
):

    model = get_model()

    text = build_text(features)

    encoding = tokenizer(

        text,

        truncation=True,

        padding=True,

        max_length=128,

        return_tensors="pt"
    )

    with torch.no_grad():

        outputs = model(

            encoding["input_ids"],

            encoding["attention_mask"]
        )

        probs = torch.softmax(
            outputs,
            dim=1
        )[0]

        pred_idx = torch.argmax(
            probs
        ).item()

    return {

        "label":
            LABELS[pred_idx],

        "confidence":
            round(
                float(probs[pred_idx]),
                4
            ),

        "probabilities": {

            LABELS[i]:
                round(
                    float(probs[i]),
                    4
                )

            for i in range(
                len(LABELS)
            )
        }
    }


# ── Feature builder ─────────────────────────────────────
def build_permission_features(
    metadata: dict,
    robots_data: dict,
    tos_data: dict
) -> dict:

    return {

        "domain":
            metadata.get("domain", ""),

        "content_type":
            metadata.get("description", ""),

        "has_robots_txt":
            robots_data.get(
                "has_robots_txt",
                "unknown"
            ),

        "robots_allows_ai":
            robots_data.get(
                "robots_allows_ai",
                "unknown"
            ),

        "robots_raw":
            robots_data.get(
                "robots_raw",
                ""
            ),

        "tos_exists":
            "yes" if tos_data.get(
                "tos_found"
            ) else "no",

        "tos_text_excerpt":
            tos_data.get(
                "tos_text",
                ""
            )[:1000],

        "requires_license":
            "no",

        "has_paywall":
            "no"
    }