from flask import Flask, request, jsonify
import yt_dlp
import os
from urllib.parse import unquote  # এটি লিঙ্ক পরিষ্কার করবে

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "API is running. Use /api?url=LINK"

@app.route('/api', methods=['GET'])
def download_video():
    # লিঙ্কটি নিয়ে সেটিকে পরিষ্কার এবং ডিকোড করা
    raw_url = request.args.get('url')
    if not raw_url:
        return jsonify({'code': 1, 'msg': 'URL is required!'}), 400
    
    video_url = unquote(raw_url).strip()
    print(f"DEBUG: Processing URL: {video_url}") # এটি রেন্ডার লগে চেক করবেন

    # কুকি ফাইলের সঠিক পাথ (Absolute path)
    cookie_path = os.path.abspath("cookies.txt")

    ydl_opts = {
        # এখানে ফরম্যাটটি আপডেট করা হয়েছে যাতে সব ভিডিও কাজ করে
        'format': 'bestvideo+bestaudio/best', 
        'quiet': True,
        'no_warnings': True,
        'cookiefile': cookie_path if os.path.exists(cookie_path) else None,
        # ব্রাউজার হিসেবে পরিচয় দেওয়ার জন্য ইউজার এজেন্ট
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            # লিঙ্ক খুঁজে পাওয়ার লজিক
            direct_link = info.get('url') or (info.get('formats')[0].get('url') if info.get('formats') else None)
            title = info.get('title', 'Social Media Video')
            thumbnail = info.get('thumbnail', 'https://img.freepik.com/free-vector/facebook-icon-vector-illustration_53876-161642.jpg')

            if not direct_link:
                return jsonify({'code': 1, 'msg': 'Could not extract direct link.'}), 400

            return jsonify({
                'code': 0,
                'data': {
                    'title': title,
                    'cover': thumbnail,
                    'play': direct_link,
                    'wmplay': direct_link,
                    'music': direct_link
                }
            })
    except Exception as e:
        return jsonify({'code': 1, 'msg': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
