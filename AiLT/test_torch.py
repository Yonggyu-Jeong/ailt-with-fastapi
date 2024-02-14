import torch, gc

try:
    gc.collect()
    torch.cuda.empty_cache()
    print("============================is_done============================")

except RuntimeError as e:
    print("============================RuntimeError============================")
