# utils.py or a suitable location
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Load model and tokenizer once (recommended for performance)
model_name = "facebook/nllb-200-distilled-600M"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

src_lang = "pes_Arab"
tgt_lang = "eng_Latn"
tokenizer.src_lang = src_lang
tgt_token_id = tokenizer.convert_tokens_to_ids(tgt_lang)

def split_by_token_limit(text, max_tokens=400):
    words = text.strip().split()
    chunks = []
    current = []
    for word in words:
        current.append(word)
        tokenized = tokenizer(" ".join(current), return_tensors="pt", truncation=False)
        if tokenized.input_ids.shape[1] >= max_tokens:
            current.pop()
            chunks.append(" ".join(current))
            current = [word]
    if current:
        chunks.append(" ".join(current))
    return chunks

def translate_chunk(chunk):
    inputs = tokenizer(chunk, return_tensors="pt", truncation=True, padding=True, max_length=512)
    outputs = model.generate(
        **inputs,
        forced_bos_token_id=tgt_token_id,
        max_new_tokens=300,
        no_repeat_ngram_size=3,
        repetition_penalty=1.5
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def to_en_nllb(textfa):
    try:
        chunks = split_by_token_limit(textfa)
        translations = [translate_chunk(chunk) for chunk in chunks]
        return " ".join(translations)
    except Exception as e:
        return f"[Translation error: {str(e)}]"
