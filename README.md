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
