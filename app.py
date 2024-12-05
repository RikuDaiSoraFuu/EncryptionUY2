from flask import Flask, request, render_template_string, send_file
import base64
import os

app = Flask(__name__)
key = b'my_secure_key_16'  # 必ず16バイト長のキーを使用

def xor_encrypt(data, key):
    encrypted = bytearray()
    for i in range(len(data)):
        encrypted.append(data[i] ^ key[i % len(key)])
    return encrypted

@app.route('/')
def index():
    # シンプルなHTMLフォームを提供
    html_form = '''
    <!doctype html>
    <title>File Encryption</title>
    <h1>Upload a file to encrypt</h1>
    <form method="POST" action="/encrypt" enctype="multipart/form-data">
        <input type="file" name="file" required>
        <button type="submit">Encrypt</button>
    </form>
    '''
    return render_template_string(html_form)

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

    # 保存
    encrypted_file_path = 'encrypted_file.txt'
    with open(encrypted_file_path, 'w') as f:
        f.write(encrypted_base64)

    return send_file(
        encrypted_file_path,
        as_attachment=True,
        download_name=f"Encrypted_{file.filename}",
        mimetype="text/plain"
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Renderの環境でPORTを取得
    app.run(host="0.0.0.0", port=port)

# from flask import Flask, request, send_file
# import base64
# import os

# app = Flask(__name__)
# key = b'my_secure_key_16'  # 必ず16バイト長のキーを使用

# def xor_encrypt(data, key):
#     encrypted = bytearray()
#     for i in range(len(data)):
#         encrypted.append(data[i] ^ key[i % len(key)])
#     return encrypted

# @app.route('/')
# def index():
#     # シンプルなHTMLフォームを提供
#     html_form = '''
#     <!doctype html>
#     <title>File Encryption</title>
#     <h1>Upload a file to encrypt</h1>
#     <form method="POST" action="/encrypt" enctype="multipart/form-data">
#         <input type="file" name="file" required>
#         <button type="submit">Encrypt</button>
#     </form>
#     '''
#     return render_template_string(html_form)
    
# @app.route('/encrypt', methods=['GET', 'POST', 'OPTIONS'])
# def encrypt():
#     if 'file' not in request.files:
#         return "No file uploaded", 400
#     file = request.files['file']
#     file_data = file.read()

#     # XOR暗号化
#     encrypted_data = xor_encrypt(file_data, key)

#     # Base64エンコード
#     encrypted_base64 = base64.b64encode(encrypted_data).decode('utf-8')

#     # 新しいファイル名を生成
#     original_filename = file.filename
#     encrypted_filename = f"Encrypted_{original_filename}"

#     # 保存
#     encrypted_file_path = os.path.join("/tmp", encrypted_filename)
#     with open(encrypted_file_path, 'w') as f:
#         f.write(encrypted_base64)

#     return send_file(
#         encrypted_file_path,
#         as_attachment=True,
#         download_name=encrypted_filename,
#         mimetype="text/plain"
#     )

# if __name__ == "__main__":
#     # Renderが指定するポートを使用
#     port = int(os.environ.get("PORT", 5000))  # デフォルトは5000
#     app.run(host="0.0.0.0", port=port)
