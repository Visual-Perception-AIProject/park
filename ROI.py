import cv2

# 1. 파일 경로 설정
video_path = 'R_video.mp4'  # 원본 영상
output_path = 'output_roi.mp4'   # 저장될 영상 이름
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("비디오를 열 수 없습니다.")
    exit()

# 영상 정보 가져오기 (저장 설정용)
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v') # 코덱 설정
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# 첫 프레임 읽기 (ROI 설정용)
ret, frame = cap.read()

# 2. 카테고리 정의
categories = [
    {"label": "Table", "color": (255, 0, 0)},    # 파랑
    {"label": "Counter", "color": (0, 255, 0)},  # 초록
    {"label": "Seat", "color": (0, 0, 255)}      # 빨강
]

roi_data = []

# 3. 순차적 ROI 선택 (여기서 카테고리가 구분됨)
for cat in categories:
    print(f"--- [{cat['label']}] 영역 선택 단계 ---")
    print("마우스 드래그로 영역 지정 -> ENTER (반복 가능) -> 완료되면 ESC")
    
    rects = cv2.selectROIs(f"Select {cat['label']}", frame, fromCenter=False, showCrosshair=True)
    
    for r in rects:
        roi_data.append({"label": cat['label'], "rect": r, "color": cat['color']})
    cv2.destroyWindow(f"Select {cat['label']}")

# 4. 영상 처리 및 저장
print("영상을 처리 중입니다. 잠시만 기다려주세요...")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 모든 ROI 정보를 바탕으로 프레임 위에 그리기
    for data in roi_data:
        x, y, w, h = map(int, data['rect'])
        cv2.rectangle(frame, (x, y), (x + w, y + h), data['color'], 2)
        cv2.putText(frame, data['label'], (x, y - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, data['color'], 2)

    # 화면에 표시
    cv2.imshow("Processing...", frame)
    
    # 영상 파일로 저장
    out.write(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print(f"저장이 완료되었습니다: {output_path}")
cap.release()
out.release()
cv2.destroyAllWindows()