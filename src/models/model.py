import numpy as np
import torch
from scipy.special import softmax
from transformers import (AutoConfig, AutoModelForSequenceClassification,
                          AutoTokenizer, logging)

MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"

logging.set_verbosity_warning()


class Roberta:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL)
        self.tokenizer.model_max_length = 512
        self.config = AutoConfig.from_pretrained(MODEL)

        # CUDA 및 MPS 지원 여부 확인
        if torch.cuda.is_available() and torch.backends.mps.is_available():
            device = torch.device(torch.backends.mps.get_default_dev())
        elif torch.cuda.is_available():
            device = torch.device("cuda")
        else:
            device = torch.device("cpu")

        print(f"Using device: {device}")

        self.model = AutoModelForSequenceClassification.from_pretrained(MODEL).to(
            device
        )

    def predict(self, text: str) -> dict[str, float]:
        encoded_input = self.tokenizer(text, return_tensors="pt")

        if encoded_input.input_ids.shape[1] > 512:
            raise Exception("Input text too long")

        output = self.model(**encoded_input)
        scores = output[0][0].detach().cpu().numpy()
        scores = softmax(scores)

        ranking = np.argsort(scores)
        ranking = ranking[::-1]

        result = {}

        for i in range(scores.shape[0]):
            label = self.config.id2label[ranking[i]]
            score = scores[ranking[i]]
            result[label] = score

        return result


roberta = Roberta()


def get_roberta() -> Roberta:
    return roberta
