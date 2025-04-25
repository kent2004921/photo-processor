import json
import base64
import cv2
import numpy as np
from rembg import remove
from io import BytesIO
from PIL import Image
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_image():
    try:
        # 从请求中获取 Base64 编码的图像
        data = request.get_json()
        image_data = base64.b64decode(data['image'])

        # 转换为 PIL 图像，供 rembg 使用
        input_image = Image.open(BytesIO(image_data))

        # 使用 rembg 去背景
        output_image = remove(input_image)

        # 转换为 OpenCV 格式（BGR）
        img_array = np.array(output_image)
        if img_array.shape[-1] == 4:  # 如果有透明通道，转换为 BGR
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGR)

        # 加载 OpenCV 的 Haar 级联分类器（人脸检测）
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) > 0:
            # 取第一个人脸
            (x, y, w, h) = faces[0]
            # 扩展裁剪区域：包含头部和部分肩膀
            x_new = max(0, x - int(w * 0.3))  # 左右扩展 30%
            y_new = max(0, y - int(h * 0.5))  # 向上扩展 50%（包含头发）
            w_new = int(w * 1.6)  # 宽度扩展 60%
            h_new = int(h * 2.0)  # 高度扩展 100%（包含肩膀）
            x_new_end = min(img_array.shape[1], x_new + w_new)
            y_new_end = min(img_array.shape[0], y_new + h_new)

            # 裁剪图像
            cropped_img = img_array[y_new:y_new_end, x_new:x_new_end]

            # 转换为 Base64 返回
            _, buffer = cv2.imencode('.png', cropped_img)
            output_base64 = base64.b64encode(buffer).decode('utf-8')

            return jsonify({'image': output_base64}), 200
        else:
            return jsonify({'error': 'No face detected'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)