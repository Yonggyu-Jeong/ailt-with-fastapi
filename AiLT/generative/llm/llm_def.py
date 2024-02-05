import torch
from transformers import pipeline, AutoModelForCausalLM

MODEL = 'beomi/KoAlpaca-Polyglot-5.8B'

model = AutoModelForCausalLM.from_pretrained(
    MODEL,
    torch_dtype=torch.float16,
    low_cpu_mem_usage=True,
).to(device=f"cuda", non_blocking=True)

pipe = pipeline(
    'text-generation',
    model=model,
    tokenizer=MODEL,
    device=0
)

