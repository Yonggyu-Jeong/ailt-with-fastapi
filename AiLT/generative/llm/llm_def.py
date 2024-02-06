import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

print(torch.cuda.is_available())

MODEL = 'beomi/llama-2-ko-7b'

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)
model = AutoModelForCausalLM.from_pretrained(MODEL, quantization_config=bnb_config, device_map={"":0})

tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL)

model.eval()
