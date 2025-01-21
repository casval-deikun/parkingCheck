from flask import Flask, jsonify
import random
# from flask_cors import CORS
app = Flask(__name__)
# CORS(app)
@app.route('/get-button-status', methods=['GET'])
def get_button_status():
    # 버튼 상태 생성 (랜덤으로 0 또는 1 할당)
    button_count = 646  # 총 버튼 개수 (예시)
    button_status = [random.randint(0, 1) for _ in range(button_count)]
    print(button_status)
    # 버튼 상태 반환
    return jsonify(button_status)

if __name__ == '__main__':
    # 디버그 모드로 서버 실행
    app.run(debug=True)
