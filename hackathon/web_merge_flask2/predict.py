# pip install torch==2.1.0
# pip install transformers==4.35.2

import torch
from transformers import BertForSequenceClassification, BertTokenizer

# 라벨 값
label_mapping = {
    0: 'Sales Rejected',
    1: 'Unqualified',
    2: 'Closed',
    3: 'Qualified',
    4: 'Converted'
}

# 저장된 모델 불러오기
model_path = '/Users/k4n9jun3/VSCode_K4n9Jun3/THU/240208/saved_Transformer_model_0207T1057PM.pth'   # 모델(.pth) 경로 정확히 설정

def prediction(input_data):
    loaded_model = torch.load(model_path, map_location=torch.device('cpu'))

    # 모델을 평가 모드로 설정
    loaded_model.eval()

    # BERT 토크나이저 로드
    tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased', do_lower_case=False)

    # 입력 데이터를 토큰화 및 패딩
    tokenized_texts = tokenizer.tokenize("[CLS] " + str(input_data) + " [SEP]")
    input_ids = tokenizer.convert_tokens_to_ids(tokenized_texts)

    # 모델에 입력 데이터를 전달하여 예측 수행
    with torch.no_grad():
        output = loaded_model(torch.tensor(input_ids).unsqueeze(0))  # unsqueeze(0)은 배치 차원 추가

    # 로짓에서 가장 높은 값의 인덱스를 찾음
    predicted_label = torch.argmax(output.logits, dim=1).item()

    label_text = label_mapping.get(predicted_label)

    return label_text

def main():
    text = input("Input Here: ")
    label = prediction(text)

    print(f"예측된 라벨: {label}")


if __name__ == "__main__":
    main()
