import os
from flask import Flask,render_template,flash,redirect,request
from markupsafe import Markup
import subprocess
import boto3
from botocore.client import Config
from dotenv import load_dotenv
from asgiref.wsgi import WsgiToAsgi

load_dotenv()

app = Flask(__name__)
app.secret_key = 'avnasjdnavnajs'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
asgi_app = WsgiToAsgi(app)

# DigitalOcean Spaces Setup.
session = boto3.session.Session()
client = session.client('s3',
                        region_name=os.getenv("DO_REGION_NAME"),
                        endpoint_url=os.getenv("DO_ENDPOINT_URL"),
                        aws_access_key_id=os.getenv("DO_KEY_ID"),
                        aws_secret_access_key=os.getenv("DO_SECRET_ID")
                        )    
BUCKET_NAME = os.getenv('BUCKET_NAME')
if not BUCKET_NAME:
    raise ValueError("❌ BUCKET_NAME is not set. Check your .env file.")

def encode(input_video,output_name,subtitle_file,selected_quality,quality,scale,crf,bv,maxrate,bufsize):
    file_compress = f'{output_name}_compress.mp4'
    
    command = [
        "ffmpeg", "-i", input_video,
        "-vf", f"scale=-2:{scale}",
        "-c:v", "libx264", "-crf", "23",
        "-preset", "fast", "-c:a", "copy",
        quality
    ]
    
    command_gpu = [
        "ffmpeg", "-i", input_video,
        "-vf", "scale=640:480",
        "-c:v", "h264_nvenc",
        "-b:v", f"{bv}k",
        "-maxrate", f"{maxrate}k",
        "-bufsize", f"{bufsize}k",
        "-c:a", "aac", "-b:a", "128k",
        quality
    ]
    
    command_compress = [
        "ffmpeg", "-i", input_video,
        "-vcodec", "libx265", "-crf", "30",
        "-preset", "fast", "-tag:v", "hvc1",
        "-acodec", "aac", "-b:a", "128k",
        file_compress
    ]
    
    escaped_subtitle = subtitle_file.replace('\\', '/').replace(':', '\\:') if subtitle_file else ""
    command_burn = [
        "ffmpeg", "-i", input_video,
        "-vf", f"subtitles='{escaped_subtitle}'",
        "-c:v", "libx264", "-crf", "23",
        "-preset", "fast", "-c:a", "aac", "-b:a", "128k",
        quality
    ]
    try:
        if selected_quality == 0: 
            subprocess.run(command_gpu,check=True, 
                            stderr=subprocess.PIPE, 
                            universal_newlines=True);
            file_size = os.path.getsize(quality)
            file_basename = os.path.basename(quality)
            client.upload_file(f'{quality}', BUCKET_NAME, f'upload/{file_basename}')
            client.put_object_acl(ACL='public-read',Bucket=BUCKET_NAME,Key=f'upload/{file_basename}')
            file_link = f'https://{BUCKET_NAME}.blr1.digitaloceanspaces.com/upload/{file_basename}'
            flash(Markup(f'✅ <strong>Success!</strong> <a class="underline text-blue-600" href="{file_link}" target="_blank">Download File</a>'), 'success')
            os.remove(quality)
            
        elif selected_quality == 4:
            subprocess.run(command_compress,check=True,
                        stderr=subprocess.PIPE,
                        universal_newlines=True)
            size_compress = os.path.getsize(file_compress)
            file_basename = os.path.basename(quality)
            client.upload_file(f'{file_compress}', BUCKET_NAME, f'upload/{file_basename}')
            client.put_object_acl(ACL='public-read',Bucket=BUCKET_NAME,Key=f'upload/{file_basename}')
            file_link = f'https://{BUCKET_NAME}.blr1.digitaloceanspaces.com/upload/{file_basename}'
            flash(Markup(f'✅ <strong>Success!</strong> <a class="underline text-blue-600" href="{file_link}" target="_blank">Download File</a>'), 'success')
            os.remove(file_compress)
        elif selected_quality == 5:
            subprocess.run(command_burn,check=True, 
                            stderr=subprocess.PIPE, 
                            universal_newlines=True);
            file_size = os.path.getsize(quality)
            file_basename = os.path.basename(quality)
            client.upload_file(f'{quality}', BUCKET_NAME, f'upload/{file_basename}')
            client.put_object_acl(ACL='public-read',Bucket=BUCKET_NAME,Key=f'upload/{file_basename}')
            file_link = f'https://{BUCKET_NAME}.blr1.digitaloceanspaces.com/upload/{file_basename}'
            flash(Markup(f'✅ <strong>Success!</strong> <a class="underline text-blue-600" href="{file_link}" target="_blank">Download File</a>'), 'success')
            os.remove(quality)
        else:
            subprocess.run(command,check=True, 
                            stderr=subprocess.PIPE, 
                            universal_newlines=True);
            file_size = os.path.getsize(quality)
            file_basename = os.path.basename(quality)
            client.upload_file(f'{quality}', BUCKET_NAME, f'upload/{file_basename}')
            client.put_object_acl(ACL='public-read',Bucket=BUCKET_NAME,Key=f'upload/{file_basename}')
            file_link = f'https://{BUCKET_NAME}.blr1.digitaloceanspaces.com/upload/{file_basename}'
            flash(Markup(f'✅ <strong>Success!</strong> <a class="underline text-blue-600" href="{file_link}" target="_blank">Download File</a>'), 'success')
            os.remove(quality)
                
    except subprocess.CalledProcessError as e:
        flash('❌ Conversion Failed!', 'danger')
    except FileNotFoundError:
        flash("\nError: FFmpeg not found. Please install FFmpeg first.",'danger')
    except Exception as e:
        flash(f"\nUnexpected error: {str(e)}",'danger')
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_file = request.files.get('input_video')
        if not video_file:
            flash("❌ Please upload a video file.", "error")
            return redirect('/')

        input_video = os.path.join(UPLOAD_FOLDER, video_file.filename)
        video_file.save(input_video)
        output_name = request.form['output_name']
        selected_quality = int(request.form['selected_mode'])
        file_480 = f'{output_name}_480.mp4'
        file_720 = f'{output_name}_720.mp4'
        file_1080 = f'{output_name}_1080.mp4'
        file_compress = f'{output_name}_compress.mp4'
    
        subtitle_file = ""
        if selected_quality == 5:
            subtitle = request.files.get('subtitle_file')
            if subtitle:
                subtitle_file = os.path.join(UPLOAD_FOLDER, subtitle.filename)
                subtitle.save(subtitle_file)
            else:
                flash("❌ Subtitle file required for Burn Subtitle Mode.", "error")
                return redirect('/')
    
        if selected_quality == 0:
                resolution = request.form.get('gpu_resolution')
                if resolution == "480":
                    encode(input_video, output_name, None, selected_quality, file_480, 480, 26, 1000, 2000, 2000)
                elif resolution == "720":
                    encode(input_video, output_name, None, selected_quality, file_720, 720, 23, 2000, 4000, 4000)
                elif resolution == "1080":
                    encode(input_video, output_name, None, selected_quality, file_1080, 1080, 20, 3000, 6000, 6000)
        elif selected_quality == 1:
                encode(input_video, output_name, None, selected_quality, file_480, 480, None, None, None, None)
        elif selected_quality == 2:
                encode(input_video, output_name, None, selected_quality, file_720, 720, None, None, None, None)
        elif selected_quality == 3:
                encode(input_video, output_name, None, selected_quality, file_1080, 1080, None, None, None, None)
        elif selected_quality == 4:
                encode(input_video, output_name, None, selected_quality, file_compress, None, None, None, None, None)
        elif selected_quality == 5:
                encode(input_video, output_name, subtitle_file, selected_quality, file_480, 480, None, None, None, None)
        try:
            os.remove(input_video)
            if subtitle_file:
                os.remove(subtitle_file)
        except:
            pass

            return redirect('/')
    return render_template('/index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)