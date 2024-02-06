from generative.llm.llm_def import tokenizer, model


def ask(x):
    answer_format = f"### 질문: {x}\n\n### 답변:"
    answer = model.generate(
        **tokenizer(
            answer_format,
            return_tensors='pt',
            return_token_type_ids=False
        ).to('cuda'),
        max_new_tokens=50,
        early_stopping=True,
        do_sample=True,
        eos_token_id=2,
    )
    print(tokenizer.decode(answer[0]))
