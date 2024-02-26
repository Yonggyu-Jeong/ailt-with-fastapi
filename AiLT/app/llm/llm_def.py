import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

print("----------------------------")
print(torch.cuda.is_available())
print("----------------------------")

LLM_MODEL = 'beomi/llama-2-ko-7b'

llm_model = AutoModelForCausalLM.from_pretrained(LLM_MODEL)
llm_tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL)

# CUDA 장치로 이동
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
llm_model.to(device)

llm_model.eval()

"""
llm_bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)
model = AutoModelForCausalLM.from_pretrained(LLM_MODEL, quantization_config=llm_bnb_config, device_map={"": 0})
"""