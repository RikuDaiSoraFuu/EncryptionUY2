from flask import Flask, request, send_file
import base64
import os

app = Flask(__name__)
key = b'my_secure_key_16'  # 必ず16バイト長のキーを使用

def xor_encrypt(data, key):
    encrypted = bytearray()
    for i in range(len(data)):
        encrypted.append(data[i] ^ key[i % len(key)])
    return encrypted

@app.route('/encrypt', methods=['POST'])
def encrypt():
    if 'file' not in request.files:
        return "No file uploaded", 400
    file = request.files['file']
    file_data = file.read()

    # XOR暗号化
    encrypted_data = xor_encrypt(file_data, key)

    # Base64エンコード
    encrypted_base64 = base64.b64encode(encrypted_data).decode('utf-8')

    # 新しいファイル名を生成
    original_filename = file.filename
    encrypted_filename = f"Encrypted_{original_filename}"

    # 保存
    encrypted_file_path = os.path.join("/tmp", encrypted_filename)
    with open(encrypted_file_path, 'w') as f:
        f.write(encrypted_base64)

    return send_file(
        encrypted_file_path,
        as_attachment=True,
        download_name=encrypted_filename,
        mimetype="text/plain"
    )

if __name__ == "__main__":
    # Renderが指定するポートを使用
    port = int(os.environ.get("PORT", 5000))  # デフォルトは5000
    app.run(host="0.0.0.0", port=port)
