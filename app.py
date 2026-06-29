from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def download_video():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({'code': 1, 'msg': 'URL is required!'}), 400

    # এখানে cookies.txt যুক্ত করা হয়েছে
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'cookiefile': 'cookies.txt', 
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            direct_link = info.get('url') or info.get('formats')[0].get('url')
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
