import os
import logging

import torch

from torch import nn

from transformers import (
    AutoTokenizer,
    AutoModel
)

from dotenv import load_dotenv

# ── Load environment variables ─────────────────────────
load_dotenv()

# ── Logging ─────────────────────────────────────────────
logger = logging.getLogger(__name__)

# ── Config ──────────────────────────────────────────────
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

MAX_LENGTH = 128

# ── Tokenizer ───────────────────────────────────────────
tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

# ── Model Architecture ──────────────────────────────────
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

        cls_embedding = (
            outputs.last_hidden_state[:, 0]
        )

        return self.fc(
            cls_embedding
        )

# ── Lazy-loaded model ───────────────────────────────────
_model = None


def get_model():

    global _model

    if _model is None:

        logger.info(
            "Loading permission model..."
        )

        if not os.path.exists(MODEL_PATH):

            raise FileNotFoundError(
                f"Permission model not found: "
                f"{MODEL_PATH}"
            )

        model = PermissionClassifier()

        checkpoint = torch.load(
            MODEL_PATH,
            map_location="cpu",
            weights_only=False
        )

        model.load_state_dict(
            checkpoint['model_state_dict']
        )

        model.eval()

        _model = model

    return _model


# ── Build inference text ────────────────────────────────
def build_text(
    features: dict
) -> str:

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
        )),

        str(features.get(
            "jurisdiction",
            ""
        ))
    ])


# ── Main inference API ──────────────────────────────────
def predict_permission(
    features: dict
):

    model = get_model()

    text = build_text(
        features
    )

    encoding = tokenizer(

        text,

        truncation=True,

        padding=True,

        max_length=MAX_LENGTH,

        return_tensors="pt"
    )

    with torch.no_grad():

        outputs = model(

            encoding["input_ids"],

            encoding["attention_mask"]
        )

        probabilities = torch.softmax(
            outputs,
            dim=1
        )[0]

        pred_idx = torch.argmax(
            probabilities
        ).item()

    return {

        "label":
            LABELS[pred_idx],

        "confidence":
            round(
                float(
                    probabilities[pred_idx]
                ),
                4
            ),

        "probabilities": {

            LABELS[i]:
                round(
                    float(probabilities[i]),
                    4
                )

            for i in range(
                len(LABELS)
            )
        }
    }

