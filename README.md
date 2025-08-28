# FastAPI Diary Project

사용자가 일기를 작성하고 AI 감정 분석 을 받을 수 있는 웹 서비스입니다.

---

## 프로젝트 목표
- 회원가입, 로그인/로그아웃 기능 구현  
- 일기 작성, 조회, 수정, 삭제  
- 일기 태그 기능  
- AI 기반 감정 요약 제공  

---

## ERD
데이터베이스 구조 확인: [dbdiagram 링크](https://dbdiagram.io/d/68ae981b1e7a611967cc2f12)  

### 테이블 설명

| 테이블 | 용도 |
|--------|-----|
| **users** | 서비스 이용 회원 정보를 저장. 이메일, 닉네임, 비밀번호, 전화번호, 관리자 여부 등 |
| **diaries** | 회원이 작성한 일기 저장. 내용, 제목, 작성 시간, 감정 분석 결과 포함 |
| **tags** | 일기 분류/주제 키워드 저장 (예: "가족", "일", "연애") |
| **diary_tags** | 일기 ↔ 태그 연결(N:M 관계) |
| **emotion_keywords** | 감정 분석 키워드 저장 (예: "불안" → "걱정돼", "긴장") |
| **diary_emotion_keywords** | 일기 ↔ 감정 키워드 연결(N:M 관계) |
| **emotion_stats** | 기간별 감정 통계 집계 (예: 지난 주 슬픔 3회, 기쁨 5회) |
| **alert_logs** | 회원에게 전송된 알림 메시지 기록 |
| **transaction_history** | 회원 포인트, 결제, 환불 내역 기록 |

### 테이블 관계 요약

| 관계 | 설명 |
|------|-----|
| users → diaries | 1:N (회원 한 명이 여러 일기 작성 가능) |
| users → emotion_stats | 1:N |
| users → alert_logs | 1:N |
| users → transaction_history | 1:N |
| diaries ↔ tags | N:M (일기 하나에 여러 태그, 태그 하나가 여러 일기에 연결) |
| diaries ↔ emotion_keywords | N:M (일기 하나에 여러 감정 키워드, 키워드 하나가 여러 일기에 사용) |
| diaries → transaction_history | 1:N (선택적, 유료 기능 사용 시 연결) |

---

## 인증(회원가입 / 로그인 / 로그아웃) 플로우

```mermaid
flowchart TD
    A[사용자] --> B[회원가입 API 호출]
    B --> C{입력 데이터 검증}
    C -->|오류 발생| D[오류 메시지 반환]
    C -->|정상| E[비밀번호 암호화]
    E --> F[DB 저장]
    F --> G[회원가입 완료 메시지]

    A --> H[로그인 API 호출]
    H --> I{이메일/비밀번호 검증}
    I -->|오류 발생| J[오류 메시지 반환]
    I -->|정상| K[JWT 토큰 발급]
    K --> L[토큰 반환]

    A --> M[로그아웃 API 호출]
    M --> N{토큰 검증}
    N -->|오류 발생| O[오류 메시지 반환]
    N -->|정상| P[블랙리스트 등록]
    P --> Q[로그아웃 완료 메시지]

API 스펙
상세 API 문서 : https://www.notion.so/25d3dc862dc380b5b525e421f75d22e0?source=copy_link