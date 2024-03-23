import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

print(torch.cuda.is_available())
TRANSLATE_MODEL = 'beomi/SOLAR-KOEN-10.8B'

tokenizer = AutoTokenizer.from_pretrained(TRANSLATE_MODEL)
model = AutoModelForCausalLM.from_pretrained(TRANSLATE_MODEL)

model.eval()
