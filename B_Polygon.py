import cv2
import json
import numpy as np
import os

# 설정 및 폴더 생성 
FOLDER_NAME = 'placeB'
video_path = 'R_video.mp4'
output_roi_file = os.path.join(FOLDER_NAME, 'roi.json')

if not os.path.exists(FOLDER_NAME):
    os.makedirs(FOLDER_NAME)

# 최종 저장 구조 
poly_output = {
    "place_id": FOLDER_NAME,
    "rois": []
}

current_points = []

def mouse_callback(event, x, y, flags, param):
    global current_points
    if event == cv2.EVENT_LBUTTONDOWN:
        current_points.append([x, y])
        cv2.circle(img_display, (x, y), 3, (0, 255, 0), -1)
        if len(current_points) > 1:
            cv2.line(img_display, tuple(current_points[-2]), tuple(current_points[-1]), (0, 255, 0), 1)
        cv2.imshow('ROI Setup', img_display)

cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()
if not ret:
    print("비디오를 불러올 수 없습니다.")
    exit()

img_display = frame.copy()
cv2.namedWindow('ROI Setup')
cv2.setMouseCallback('ROI Setup', mouse_callback)

print("--- ROI 설정 방법 ---")
print("1. 마우스 왼쪽 클릭: 점 찍기")
print("2. 't' 키: 현재 영역을 Table(Txx)로 저장")
print("3. 's' 키: 현재 영역을 Seat(Sxx)로 저장")
print("4. 'c' 키: 현재 영역을 Counter(Cxx)로 저장") 
print("5. 'r' 키: 현재 찍고 있는 점 초기화")         
print("6. 'q' 키: 완료 및 저장 후 종료")

# 카운터
t_count = 1
s_count = 1
c_count = 1

while True:
    cv2.imshow('ROI Setup', img_display)
    key = cv2.waitKey(1) & 0xFF

    # T(Table), S(Seat), C(Counter) 키 입력 처리
    if key in [ord('t'), ord('s'), ord('c')]:
        if len(current_points) < 3:
            print("최소 3개 이상의 점을 찍어야 합니다.")
            continue
        
        # 라벨 결정 로직
        if key == ord('t'):
            label = f"T{t_count:02d}"
            t_count += 1
        elif key == ord('s'):
            label = f"S{s_count:02d}"
            s_count += 1
        elif key == ord('c'):
            label = f"C{c_count:02d}"
            c_count += 1
        
        poly_output["rois"].append({
            "label": label,
            "type": "Polygon",  
            "points": current_points
        })
        
        # 화면 업데이트
        cv2.polylines(frame, [np.array(current_points)], True, (255, 0, 0), 2)
        cv2.putText(frame, label, tuple(current_points[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        img_display = frame.copy()
        current_points = []
        print(f"{label} 저장 완료.")

    elif key == ord('r'):
        current_points = []
        img_display = frame.copy()
        print("입력 초기화.")

    elif key == ord('q'):
        break

# 결과 저장 
with open(output_roi_file, 'w', encoding='utf-8') as f:
    json.dump(poly_output, f, indent=4, ensure_ascii=False)

cap.release()
cv2.destroyAllWindows()
print(f"ROI 정보가 {output_roi_file}에 저장되었습니다.")