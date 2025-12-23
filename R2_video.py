import cv2
import os
import re

def create_video_from_images(R2_images, R2_video, fps):
    # 1. 이미지 파일 목록 가져오기 및 정렬
    images = [img for img in os.listdir(R2_images) 
            if 'jpg' in img.lower() or 'png' in img.lower() or 'jpeg' in img.lower()]

    if not images:
        print("이미지 폴더가 비어있습니다.")
        return
    
    images.sort(key=lambda x: int(re.search(r'-(\d+)_', x).group(1)) if re.search(r'-(\d+)_', x) else 0)

    # 2. 첫 번째 이미지를 읽어 기본 크기(Width, Height) 설정
    first_image_path = os.path.join(R2_images, images[0])
    frame = cv2.imread(first_image_path)
    height, width, layers = frame.shape

    # 3. 비디오 라이터 설정
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    video = cv2.VideoWriter(R2_video, fourcc, fps, (width, height))

    for image in images:
        img_path = os.path.join(R2_images, image)
        frame = cv2.imread(img_path)
        
        # 4. 모든 이미지를 첫 번째 이미지 크기로 강제 리사이즈
        frame_resized = cv2.resize(frame, (width, height))
        
        video.write(frame_resized)
        print(f"{image} 추가 중...")

    video.release()
    print(f"--- 영상 제작 완료: {R2_video} ---")

create_video_from_images('R2_images', 'R2_video.mp4', fps=3)