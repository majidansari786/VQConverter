import os
import subprocess
def quality():
    input_video = input('Enter Video address:')
    output_name = input("Enter video name:")
    selected_quality = int(input("Enter Number Which Quality To convert: \n 0 for Gpu Mode \n 1 for 480 \n 2 for 720 \n 3 for 1080 \n if you all quality then Enter 4 \n 5 for compression \nWhat you want? :"))
    file_480 = f'{output_name}_480.mp4'
    file_720 = f'{output_name}_720.mp4'
    file_1080 = f'{output_name}_1080.mp4'
    file_compress = f'{output_name}_compress.mp4'
    
    command_480p = f'ffmpeg -i {input_video} -vf "scale=-2:480" -c:v libx264 -crf 23 -preset fast -c:a copy {file_480}'
    command_720p = f'ffmpeg -i {input_video} -vf "scale=-2:720" -c:v libx264 -crf 23 -preset fast -c:a copy {file_720}'
    command_1080p = f'ffmpeg -i {input_video} -vf "scale=-2:1080" -c:v libx264 -crf 23 -preset fast -c:a copy {file_1080}'
    command_480p_gpu = f'ffmpeg -i "{input_video}" -vf "scale=640:480" -c:v h264_nvenc -b:v 1000k -maxrate 1000k -bufsize 2000k -c:a aac -b:a 128k "{file_480}"'
    command_720p_gpu = f'ffmpeg -i "{input_video}" -vf "scale=1280:720" -c:v h264_nvenc -b:v 2000k -maxrate 2000k -bufsize 4000k -c:a aac -b:a 128k "{file_720}"'
    command_1080p_gpu = f'ffmpeg -i "{input_video}" -vf "scale=1920:1080" -c:v h264_nvenc -b:v 3000k -maxrate 3000k -bufsize 6000k -c:a aac -b:a 128k "{file_1080}"'
    command_compress = f'ffmpeg -i {input_video} -vcodec libx265 -crf 30 -preset fast -tag:v hvc1 -acodec aac -b:a 128k {file_compress}'
    try:
        if selected_quality == 0: 
            choice = int(input('Only 8 bit video can be encoded in Gpu Mode: \n 1) 480 \n 2) 720 \n 3) 1080\n Enter number:'))
            if choice == 1:
                subprocess.run(command_480p_gpu,check=True, 
                              stderr=subprocess.PIPE, 
                              universal_newlines=True);
                size_480 = os.path.getsize(file_480)
                print("\n" + "="*50)
                print("✅ Conversion Successful!")
                print(f"Generated Files: \n{file_480}: {size_480/(1024*1024):.2f} MB")
                print("="*50)
            elif choice == 2:
                subprocess.run(command_720p_gpu,check=True, 
                              stderr=subprocess.PIPE, 
                              universal_newlines=True);
                size_720 = os.path.getsize(file_720)
                print("\n" + "="*50)
                print("✅ Conversion Successful!")
                print(f"Generated Files: \n{file_720}: {size_720/(1024*1024):.2f} MB")
                print("="*50)
            elif choice == 3:
                subprocess.run(command_1080p_gpu,check=True, 
                              stderr=subprocess.PIPE, 
                              universal_newlines=True);
                size_1080 = os.path.getsize(file_1080)
                print("\n" + "="*50)
                print("✅ Conversion Successful!")
                print(f"Generated Files: \n{file_1080}: {size_1080/(1024*1024):.2f} MB")
                print("="*50)
        elif selected_quality == 1:
            subprocess.run(command_480p,check=True, 
                              stderr=subprocess.PIPE, 
                              universal_newlines=True);
            size_480 = os.path.getsize(file_480)
            print("\n" + "="*50)
            print("✅ Conversion Successful!")
            print(f"Generated Files: \n{file_480}: {size_480/(1024*1024):.2f} MB")
            print("="*50)
        elif selected_quality == 2:
            subprocess.run(command_720p,check=True, 
                              stderr=subprocess.PIPE, 
                              universal_newlines=True);
            size_720 = os.path.getsize(file_720)
            print("\n" + "="*50)
            print("✅ Conversion Successful!")
            print(f"Generated Files: \n{file_720}: {size_720/(1024*1024):.2f} MB")
            print("="*50)
        elif selected_quality == 3:
            subprocess.run(command_1080p,check=True, 
                              stderr=subprocess.PIPE, 
                              universal_newlines=True);
            size_1080 = os.path.getsize(file_1080)
            print("\n" + "="*50)
            print("✅ Conversion Successful!")
            print(f"Generated Files: \n{file_1080}: {size_1080/(1024*1024):.2f} MB")
            print("="*50)
        elif selected_quality == 4:
            subprocess.run(command_480p,check=True, 
                              stderr=subprocess.PIPE, 
                              universal_newlines=True);
            subprocess.run(command_720p,check=True, 
                              stderr=subprocess.PIPE, 
                              universal_newlines=True);
            subprocess.run(command_1080p,check=True, 
                              stderr=subprocess.PIPE, 
                              universal_newlines=True);
            size_480 = os.path.getsize(file_480)
            size_720 = os.path.getsize(file_720)
            size_1080 = os.path.getsize(file_1080)
            print("\n" + "="*50)
            print("✅ Conversion Successful in 3 Qualities!")
            print(f"Generated Files: \n{file_480}: {size_480/(1024*1024):.2f} MB, \n{file_720}: {size_720/(1024*1024):.2f} MB,\n{file_1080}: {size_1080/(1024*1024):.2f} MB")
            print("="*50)
        elif selected_quality == 5:
            subprocess.run(command_compress,check=True,
                           stderr=subprocess.PIPE,
                           universal_newlines=True)
            size_compress = os.path.getsize(file_compress)
            print("\n" + "="*50)
            print("✅ Compression Successful!")
            print(f"Generated Files: \n{file_compress}: {size_compress/(1024*1024):.2f} MB")
            print("="*50)
    except subprocess.CalledProcessError as e:
        print("\n" + "="*50)
        print("❌ Conversion Failed!")
        print(f"Error: {e.stderr.splitlines()[-1] if e.stderr else 'Unknown error'}")
        print("="*50)
    except FileNotFoundError:
        print("\nError: FFmpeg not found. Please install FFmpeg first.")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        
quality()