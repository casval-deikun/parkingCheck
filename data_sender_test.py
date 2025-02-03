import requests
import random
import time
import json

# Lambda URL (API Gateway의 엔드포인트)
LAMBDA_URL = "https://r5gxctlmk5whdbbdshppch2phi0lhfbq.lambda-url.ap-northeast-2.on.aws//update-button-status"

def generate_button_status():
    # 646개의 버튼 상태를 랜덤으로 생성 (0 또는 1)
    return [random.randint(0, 1) for _ in range(646)]

def send_button_status():
    button_status = generate_button_status()
    
    # POST 요청 보내기
    try:
        response = requests.post(LAMBDA_URL, json=button_status)
        if response.status_code == 200:
            print("Button status updated successfully.")
        else:
            print("Failed to update button status.")
    except Exception as e:
        print(f"Error sending data to Lambda: {e}")

# 5초마다 Lambda에 데이터 전송
while True:
    send_button_status()
    time.sleep(5)  # 5초 간격으로 반복
