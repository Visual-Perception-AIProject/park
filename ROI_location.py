import cv2
import json

# 1. 파일 경로 설정
video_path = 'R_video.mp4'
output_path = 'output_roi.mp4'
json_path = 'ROI_location.json'  # 저장될 JSON 파일 이름

cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("비디오를 열 수 없습니다.")
    exit()

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

ret, frame = cap.read()

# 2. 카테고리 정의
categories = [
    {"label": "Table", "color": (255, 0, 0)},
    {"label": "Counter", "color": (0, 255, 0)},
    {"label": "Seat", "color": (0, 0, 255)}
]

roi_data_list = []  # JSON 저장용 리스트

# 3. 순차적 ROI 선택 및 좌표 변환
for cat in categories:
    print(f"--- [{cat['label']}] 영역 선택 단계 ---")
    rects = cv2.selectROIs(f"Select {cat['label']}", frame, fromCenter=False, showCrosshair=True)
    
    for r in rects:
        x, y, w, h = map(int, r)
        
        # 사용자가 요청한 x1, y1, x2, y2 구조로 변환
        roi_item = {
            "label": cat['label'],
            "bbox": {
                "x1": x,
                "y1": y,
                "x2": x + w,
                "y2": y + h
            },
            "color": cat['color'] # 영상 출력용 색상 보관
        }
        roi_data_list.append(roi_item)
    
    cv2.destroyWindow(f"Select {cat['label']}")

# 4. JSON 파일 저장 (영상 처리 전 저장)
with open(json_path, 'w', encoding='utf-8') as f:
    # 색상 정보(color)는 제외하고 좌표 데이터만 깔끔하게 저장
    json_save_data = [
        {"label": item["label"], "bbox": item["bbox"]} 
        for item in roi_data_list
    ]
    json.dump(json_save_data, f, indent=4, ensure_ascii=False)

print(f"JSON 좌표 파일 저장 완료: {json_path}")

# 5. 영상 처리 및 저장 (저장된 리스트 활용)
print("영상을 처리 중입니다...")
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    for data in roi_data_list:
        b = data['bbox']
        color = data['color']
        label = data['label']
        
        # 사각형 그리기 (x1, y1) -> (x2, y2)
        cv2.rectangle(frame, (b['x1'], b['y1']), (b['x2'], b['y2']), color, 2)
        cv2.putText(frame, label, (b['x1'], b['y1'] - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    out.write(frame)
    cv2.imshow("Processing...", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()