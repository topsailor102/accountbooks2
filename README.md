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

## 보안 주의사항

⚠️ **중요**: `secrets.json` 파일은 절대 Git에 커밋하지 마세요!
- 이 파일은 `.gitignore`에 포함되어 있습니다.
- 대신 `secrets.json.example` 파일을 참고하여 각 환경에서 생성하세요.
