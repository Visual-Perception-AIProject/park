import cv2
import json
import os

# 설정 값 및 폴더 생성 
FOLDER_NAME = 'placeA'
video_path = 'R2_video.mp4'
output_jsonl = os.path.join(FOLDER_NAME, 'gt_people.jsonl')
frame_limit = 40 

if not os.path.exists(FOLDER_NAME):
    os.makedirs(FOLDER_NAME)

cap = cv2.VideoCapture(video_path)
frame_idx = 0

with open(output_jsonl, 'w', encoding='utf-8') as f:
    while frame_idx < frame_limit:
        ret, frame = cap.read()
        if not ret: break

        print(f"현재 프레임: {frame_idx} (사람 영역을 드래그한 후 ENTER, 프레임 종료 시 ESC)")
        
        # OpenCV ROI 선택기 사용
        rects = cv2.selectROIs('Annotation', frame, fromCenter=False, showCrosshair=True)
        
        frame_coordinates = []
        for rect in rects:
            x, y, w, h = [int(v) for v in rect]
            frame_coordinates.append([x, y, x + w, y + h])
        
        # 요구사항
        data = {
            "frame_id": frame_idx, 
            "coordinates": frame_coordinates
        }
        
        # 한 줄씩 저장 (JSONL)
        f.write(json.dumps(data, ensure_ascii=False) + '\n')
        
        frame_idx += 1
        if cv2.waitKey(1) & 0xFF == ord('q'): # 중간 종료 옵션
            break

cap.release()
cv2.destroyAllWindows()
print(f"어노테이션이 {output_jsonl}에 저장되었습니다.")