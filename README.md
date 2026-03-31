# Antigravity - Django Account Book

Django 기반 가계부 애플리케이션입니다.

## 설정 방법

### 1. 환경 설정

```bash
# Conda 환경 생성 및 활성화
conda create -n antigravity python=3.12
conda activate antigravity

# 의존성 설치
conda install django pymysql -c conda-forge -y
```

### 2. Secrets 파일 설정

`secrets.json.example` 파일을 복사하여 `secrets.json`을 생성하고 실제 값으로 수정하세요:

```bash
cp secrets.json.example secrets.json
```

`secrets.json` 파일을 열어 다음 항목들을 수정하세요:
- `SECRET_KEY`: Django 시크릿 키
- `DATABASE`: MariaDB/MySQL 연결 정보
  - `NAME`: 데이터베이스 이름
  - `USER`: 데이터베이스 사용자
  - `PASSWORD`: 데이터베이스 비밀번호
  - `HOST`: 데이터베이스 호스트
  - `PORT`: 데이터베이스 포트

### 3. 데이터베이스 마이그레이션

```bash
python manage.py migrate
```

### 4. 서버 실행

```bash
# 방법 1: 스크립트 사용
./run.sh

# 방법 2: 직접 실행
python manage.py runserver 0.0.0.0:8123
```

## 주요 기능

- 지출 내역 관리 (추가, 수정, 삭제)
- 월간/연간 소비 통계
- CSV 파일 업로드를 통한 일괄 등록
- 대시보드 및 차트 시각화
- 사용자 인증 (로그인/로그아웃)

## UI (프론트엔드) 아키텍처

이 가계부 앱은 Bootstrap과 같은 무거운 외부 프레임워크에 의존하지 않고, 독자적인 **순수 모던 CSS(Vanilla CSS)** 디자인 시스템 기반으로 작성되었습니다.

- **스타일 시트**: `records/static/css/main.css`
- **주요 특징**:
  - CSS 변수(`:root`)를 활용한 일관된 컬러 팔레트 및 타이포그래피(Inter 폰트 등) 통제
  - 글래스모피즘(Glassmorphism) 등 최신 트렌드가 반영된 UI 카드 컴포넌트(`glass-card`)
  - CSS Flexbox 및 Grid를 이용한 직관적인 시맨틱(Semantic) 반응형 레이아웃
  - **데이터 시각화 (Chart.js 최신화)**: 구형 v2 엔진 대신 성능이 향상되고 모듈화가 잘 된 **Chart.js 최고버전(v4)**으로 고도화 마이그레이션을 적용하여, 사용자가 시각적으로 편안함을 느끼는 캔버스(Canvas) UI 형식을 안정적으로 유지.

## 보안 주의사항

⚠️ **중요**: `secrets.json` 파일은 절대 Git에 커밋하지 마세요!
- 이 파일은 `.gitignore`에 포함되어 있습니다.
- 대신 `secrets.json.example` 파일을 참고하여 각 환경에서 생성하세요.

## 데이터베이스 연결 최적화 (성능 향상 방안)

이 프로젝트는 접속 시 발생하는 속도 지연(오버헤드 및 Hang)을 방지하기 위해 다음 두 가지 설정을 적극 권장합니다.

### 1. Django `CONN_MAX_AGE` 설정 (Connection Pooling)
장고는 매 요청마다 데이터베이스에 새롭게 접속하는 데 엄청난 시간을 소모합니다. 연결을 유지하고 재사용하기 위해, `secrets.json`의 `DATABASE` 설정에 `"CONN_MAX_AGE": 60` (초 단위)을 추가합니다.

### 2. Synology MariaDB `skip-name-resolve` 설정 (DNS 역참조 대기 방지)
데이터베이스 서버가 접속을 받을 때마다 DNS 이름을 확인하느라 멈추는 현상을 방지합니다. 
시놀로지 기반 MariaDB 10 패키지의 경우 기본 설정 파일이 읽기 전용이므로, 다음 과정을 거쳐 커스텀 설정을 오버라이드합니다:

1. NAS에 관리자 권한으로 터미널(SSH) 접속
2. `sudo vi /var/packages/MariaDB10/etc/my.cnf` 입력
3. `[mysqld]` 와 그 아래에 `skip-name-resolve` 내용 추가 후 저장 (`:wq`):
   ```ini
   [mysqld]
   skip-name-resolve
   ```
4. 시놀로지의 패키지 센터에서 **MariaDB 10** 앱을 [중지]한 뒤 다시 [실행]하여 적용 완료

## 최근 변경 이력 (Changelog)

- **UI 프론트엔드 모던화**: 기존 Bootstrap 및 SB Admin 2 테마를 완전 제거하고 `main.css` 기반의 Vanilla CSS와 글래스모피즘(Glassmorphism) 테마로 마이그레이션.
- **결제수단 선택지(Way) 튜닝**: 사용하지 않는 결제 수단('ING') 항목을 과거 데이터 삭제 없이 지출 입력 폼(ExpenseForm)의 드롭다운 목록에서만 보이지 않도록 제외(Exclude) 처리.
- **데이터 시각화 업그레이드 및 레이아웃 픽스**: 
  - Chart.js 무거운 구버전(v2.9)을 최신 렌더링 엔진인 Chart.js v4로 롤백 및 업그레이드. 
  - Chart.js 최신 버전에 반응형 크기(`maintainAspectRatio: false`)를 적용할 경우 Y축 높이가 찌그러지는 버그를 해결하기 위해, 모든 캔버스 부모 레이아웃 컨테이너에 `height: 400px`를 부여하는 스타일 픽스 적용 완료.
- **모바일 풀 반응형(Responsive) 최적화 도입**: 브라우저 창 조절 시 레이아웃이 유기적으로 가변하도록 미디어 쿼리(`@media`)를 새롭게 적용.
  - 모바일 해상도(768px 이하)에서 고정 사이드바가 자동으로 좌측 밖으로 숨겨지며, 상단에 슬라이드를 제어할 수 있는 햄버거 토글 메뉴(≡) 추가.
  - CSS Flex/Grid 내부 자식(Chart.js 엔진)의 크기 제약에 의한 사이드 스크롤 발생을 막기 위해 뷰포트 컨테이너에 `min-width: 0` 속성을 일괄 부여하여 유연성을 크게 개선.
