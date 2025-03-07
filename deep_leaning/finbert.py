from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline


### 함수 기본세팅 정의
finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone', num_labels=3)
tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
nlp = pipeline("sentiment-analysis", model=finbert, tokenizer=tokenizer)


## 함수에 집어넣을 것 1행 씩 처리 해서  반복
'''
csv에서 텍스트를 가져와서 > df 로 만들고  

# '''
#     for 

#         #실제로 돌가는 함수 반복
#         results = nlp(sentences)
#         print(results)

#         # df finbert_label rlfhrgownj. 
#         print(results)


# print(results)
