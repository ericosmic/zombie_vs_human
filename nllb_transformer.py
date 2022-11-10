
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser('NLLB Demo')
    parser.add_argument('--lang', '-l', type=str)
    parser.add_argument('--target_lang','-tl', type=str)
    parser.add_argument('--sentence', '-s', type=str)
    args = parser.parse_args()
    print(args.__dict__)
    tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M", use_auth_token=False, src_lang=\
        args.lang)
    model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M", use_auth_token=False)

    article = args.sentence #"Şeful ONU spune că nu există o soluţie militară în Siria"
    inputs = tokenizer(article, return_tensors="pt")

    translated_tokens = model.generate(
        **inputs, forced_bos_token_id=tokenizer.lang_code_to_id[args.target_lang], max_length=30
        )
    translated_result = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]

    print(f'translation_result: {translated_result}')
















