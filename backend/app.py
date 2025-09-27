import base64
import io
import qrcode
from PIL import Image
from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from backend.sheet_manager import SheetManager
import os

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# Google Sheets API setup
# Move instantiation to use SheetManager
spreadsheet_name = "QR Attendance Records" # This will be your main spreadsheet
creds_file_path = os.path.join(os.path.dirname(__file__), 'creds.json')
sheet_manager = SheetManager(creds_file_path, spreadsheet_name)

# Remove the old try-except block for sheet initialization
# The sheet_manager will handle connection logic

# @app.route('/')
# def home():
#     return "Welcome to the QR Attendance Backend!"
# Optional: /teacher route bhi
@app.route('/teacher')
def teacher():
    return send_from_directory(app.static_folder, 'teacher.html')

@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'teacher.html')

@app.route('/generate_qr', methods=['GET'])
def generate_qr():
    data = request.args.get('data')
    if not data:
        return jsonify({'error': 'Missing data parameter'}), 400

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    return jsonify({'qr_code': image_base64})

@app.route('/create_session_sheet', methods=['POST'])
def create_session_sheet():
    data = request.get_json()
    session_name = data.get('session_name')

    if not session_name:
        return jsonify({'error': 'Missing session_name parameter'}), 400

    if not sheet_manager.spreadsheet:
        return jsonify({'error': 'Google Sheets connection failed at startup.'}), 500

    worksheet = sheet_manager.create_session_sheet(session_name)
    if worksheet:
        return jsonify({'message': f'Session sheet \'{session_name}\' created successfully.', 'sheet_url': worksheet.url}), 200
    else:
        return jsonify({'error': f'Failed to create session sheet \'{session_name}\'.'}), 500

@app.route('/submit_attendance', methods=['POST'])
def submit_attendance():
    data = request.get_json()
    name = data.get('name')
    roll_number = data.get('roll_number')
    # qr_data now contains the session name
    session_name = data.get('qr_data')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not all([name, roll_number, session_name]):
        return jsonify({'error': 'Missing attendance data (name, roll number, or session name).'}), 400

    if not sheet_manager.spreadsheet:
        return jsonify({'error': 'Google Sheets connection failed at startup.'}), 500

    success, is_duplicate, sessions_attended = sheet_manager.record_attendance(session_name, name, roll_number, timestamp)

    if success:
        if is_duplicate:
            return jsonify({'message': f'Attendance already marked for this session. Total sessions: {sessions_attended}', 'sessions_attended': sessions_attended, 'is_duplicate': True}), 200
        else:
            return jsonify({'message': 'Attendance submitted successfully!', 'sessions_attended': sessions_attended, 'is_duplicate': False}), 200
    else:
        return jsonify({'error': 'Failed to submit attendance.'}), 500

if __name__ == '__main__':
    app.run(debug=True)


