# irumi-backend

## 초기 셋팅
### 가상환경 생성
    windows : python -m venv {가상 환경 이름}
    mac : python3 -m venv {가상 환경 이름}
    * 가상 환경 이름은 venv로 통일

### 가상환경 실행
    windows : source venv/Scripts/activate
    mac : source venv/bin/activate


### 라이브러리 설치
    pip install -r requirements.txt

    * 추가된 pip 어쩌구 있으면 'pip freeze > requirements.txt' 명령어 꼭 사용

### db 마이그레이션 진행
    * manage.py 파일이 있는 위치로 이동 후
    python manage.py makemigrations
    python manage.py migrate

### 서버 실행
    python manage.py runserver

## 🎯 Commit Convention

-   feat : 새로운 기능 추가
-   fix : 버그 수정
-   docs : 문서 수정
-   style : 코드 포맷팅, 세미콜론 누락, 코드 변경이 없는 경우
-   refactor: 코드 리펙토링
-   test: 테스트 코드, 리펙토링 테스트 코드 추가
-   chore : 빌드 업무 수정, 패키지 매니저 수정


## 💡 PR Convetion

| 아이콘 | 코드                       | 설명                     |
| ------ | -------------------------- | ------------------------ |
| 🎨     | :art                       | 코드의 구조/형태 개선    |
| ⚡️    | :zap                       | 성능 개선                |
| 🔥     | :fire                      | 코드/파일 삭제           |
| 🐛     | :bug                       | 버그 수정                |
| 🚑     | :ambulance                 | 긴급 수정                |
| ✨     | :sparkles                  | 새 기능                  |
| 💄     | :lipstick                  | UI/스타일 파일 추가/수정 |
| ⏪     | :rewind                    | 변경 내용 되돌리기       |
| 🔀     | :twisted_rightwards_arrows | 브랜치 합병              |
| 💡     | :bulb                      | 주석 추가/수정           |
| 🗃      | :card_file_box             | 데이버베이스 관련 수정   |