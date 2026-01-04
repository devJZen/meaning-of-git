# git-log-hack

**한국어** | **[English](README_EN.md)**

---

## 개요

GitHub 잔디밭(contribution graph)은 **Author Date**를 기준으로 그려지므로 과거와 미래의 기여도를 모두 통제할 수 있습니다.

이 프로젝트는 Git 커밋 날짜를 조작하여 GitHub 잔디밭에 원하는 패턴을 그리는 방법을 보여줍니다.

![Example Pattern](https://img.shields.io/badge/Pattern-Customizable-green)

## 빠른 사용법

```bash
# 1. 패턴 디자인 (대화형 에디터)
cd interactive-cli
python3 github_canvas.py
# → 방향키로 이동, Space로 칠하기, S로 저장, Q로 종료

# 2. Git 커밋 생성
python3 git_generator.py generate pattern.json 2024

# 3. GitHub에 푸시
cd ..
git push -f origin main
```

> **중요**: `github_canvas.py`는 패턴 디자인만, `git_generator.py`는 실제 커밋 생성을 담당합니다.

## 작동 원리

GitHub 잔디밭은 다음 메커니즘으로 생성됩니다:

1. **로컬에서 커밋 생성**: 클라이언트에서 `GIT_AUTHOR_DATE`와 `GIT_COMMITTER_DATE`를 사용하여 날짜를 자유롭게 설정할 수 있습니다
2. **서버에 저장**: GitHub(및 다른 Git 플랫폼)은 받은 커밋의 날짜를 검증 없이 저장합니다
3. **검증 없음**: 서버는 타임스탬프의 진위를 검증하지 않습니다

**모든 Git 플랫폼에 적용됩니다**: GitHub, GitLab, Bitbucket, Gitea 등

### 기술적 세부사항

```bash
# 커스텀 날짜로 커밋 생성
GIT_AUTHOR_DATE="2024-01-15 10:00:00" \
GIT_COMMITTER_DATE="2024-01-15 10:00:00" \
git commit -m "과거 날짜 커밋"
```

잔디밭은 커밋 생성 시각이나 푸시 시각이 아닌 **Author Date**를 기준으로 표시됩니다.

## 기능

### 1. 기본 스크립트

`create_flower_commits.py`로 간단한 패턴 생성

```bash
python3 create_flower_commits.py
```

### 2. 대화형 캔버스 에디터

터미널 기반 대화형 에디터로 커스텀 패턴 그리기

```bash
cd interactive-cli
python3 github_canvas.py
```

**기능**:

- 실시간 패턴 미리보기
- 5단계 강도 조절 (일일 커밋 0-4개)
- 2가지 표시 스타일 (음영/블록)
- 패턴 저장/불러오기 (JSON 형식)
- Git 커밋 자동 생성

**키 조작법**:

- 방향키: 커서 이동
- Space: 강도 토글 (0→1→2→3→4→0)
- 0-4: 직접 강도 설정
- T: 표시 스타일 변경
- S: 패턴 저장
- L: 패턴 불러오기
- C: 캔버스 초기화
- Q/ESC: 종료

자세한 사용법은 [interactive-cli/README.md](interactive-cli/README.md)를 참고하세요.

## 예제

```
55fd317 - devJZen, 1년 전 : Flower commit 52
7e81ed7 - devJZen, 12달 전 : Flower commit 51
341ddee - devJZen, 1년 전 : Flower commit 50
b2c4066 - devJZen, 1년 전 : Flower commit 49
9af3713 - devJZen, 1년 전 : Flower commit 48
```

## 프로젝트 구조

```
git-log-hack/
├── create_flower_commits.py    # 간단한 꽃 패턴 스크립트
├── interactive-cli/             # 대화형 캔버스 에디터
│   ├── github_canvas.py        # 터미널 기반 패턴 에디터
│   ├── git_generator.py        # 패턴 → Git 커밋 변환기
│   ├── patterns/               # 저장된 패턴 파일
│   └── README.md               # 상세 사용 가이드
├── README.md                   # 이 파일 (한국어)
└── README_EN.md                # 영어 버전
```

## 강도 레벨

- **0**: 비어있음 (커밋 없음)
- **1**: 연한 초록 (1-3개 커밋)
- **2**: 중간 초록 (4-7개 커밋)
- **3**: 진한 초록 (8-12개 커밋)
- **4**: 매우 진한 초록 (13-20개 커밋)

## 연구 & 실험

이 프로젝트는 Git 날짜 조작에 대한 광범위한 연구를 포함합니다:

### 성공한 실험 ✅

- **커밋 날짜 조작**: 완벽하게 작동
- **과거 날짜 PR**: 머지 시 커밋 날짜 유지됨
- **Wiki 날짜 조작**: 작동하지만 잔디밭에는 반영 안됨

### 한계 ❌

- **PR 생성 날짜**: 소급 적용 불가능 (서버에서 생성)
- **PR 머지 날짜**: 소급 적용 불가능
- **Issue 생성 날짜**: 소급 적용 불가능 (API 제한)
- **Star 날짜**: 조작 불가능하며 시도 시 약관 위반

연구 문서:

- `git-date-commands-research.md` - Git 날짜 조작 가능한 모든 명령어
- `pr-creation-date-research.md` - PR 생성 날짜 조작 연구
- `test-pr-experiment.md` - PR 날짜 조작 실험 결과
- `wiki-experiment.md` - Wiki 날짜 조작 실험 결과

## 주의사항

### ⚠️ 경고

1. **`git push -f`는 히스토리를 덮어씁니다**: 중요한 저장소에는 사용하지 마세요
2. **이메일 설정**: git 이메일이 GitHub 계정과 일치해야 합니다
   ```bash
   git config user.email "your-github@email.com"
   ```
3. **프라이빗 리포지토리**: "Private contributions" 설정 활성화 필요할 수 있음
4. **패턴 크기**: 7줄 (요일) × 52칸 (주)

### 윤리적 고려사항

이 프로젝트는 다음을 위한 것입니다:

- ✅ 교육 목적
- ✅ Git 내부 구조 이해
- ✅ 자신의 프로필에 재미있는 패턴 만들기
- ✅ 분산 시스템의 신뢰 모델 시연

이 프로젝트는 다음을 위한 것이 아닙니다:

- ❌ 취업을 위한 허위 경력 조작
- ❌ 기여도 통계 오도
- ❌ GitHub 서비스 약관 위반

## GitHub 잔디밭 작동 방식

**기여도로 인정되는 것**:

- ✅ 커밋 (Author Date 기준)
- ✅ Pull Request 생성
- ✅ Issue 생성
- ✅ 코드 리뷰

**인정되지 않는 것**:

- ❌ PR 머지 날짜
- ❌ 머지 커밋 (일반 커밋으로 표시됨)
- ❌ Wiki 커밋 (날짜 조작은 가능하지만 잔디밭에 반영 안됨)
- ❌ 포크 커밋 (포크 소유자가 아닌 경우)

**사용되는 날짜**: Author Date (`GIT_AUTHOR_DATE`), Committer Date나 푸시 시각 아님

## 자주 묻는 질문 (FAQ)

**Q: 계정이 정지될 수 있나요?**
A: 커밋 날짜 조작 자체는 GitHub 약관 위반이 아닙니다. 다만 책임감 있게 사용하세요.

**Q: PR이 왜 커밋으로 표시되나요?**
A: GitHub 잔디밭은 커밋을 추적하지 PR 머지 이벤트를 추적하지 않습니다. PR 내의 커밋들이 Author Date 기준으로 개별적으로 계산됩니다.

**Q: PR 생성 날짜를 과거로 할 수 있나요?**
A: 아니요, PR 생성 타임스탬프는 서버에서 생성되며 수정할 수 없습니다.

**Q: 프라이빗 리포지토리에서도 작동하나요?**
A: 네, 하지만 GitHub 설정에서 "Private contributions"를 활성화해야 할 수 있습니다.

**Q: 다른 Git 플랫폼에서도 사용할 수 있나요?**
A: 네! GitLab, Bitbucket 등 다른 플랫폼도 커밋 날짜 기반의 유사한 활동 그래프를 사용합니다.

## 고급 사용법

### 여러 연도에 걸친 커밋 생성

```bash
python3 git_generator.py generate pattern.json 2023
python3 git_generator.py generate pattern.json 2024
```

### 생성 전 패턴 미리보기

```bash
python3 git_generator.py preview pattern.json
```

### 커스텀 패턴 파일

패턴은 JSON 형식으로 저장됩니다:

```json
{
  "grid": [
    [0, 0, 1, 0, 0, ...],
    [0, 1, 2, 1, 0, ...],
    ...
  ],
  "width": 52,
  "height": 7,
  "created": "2024-12-31T09:00:00"
}
```

## 연구 문서

- `git-date-commands-research.md` - Git 날짜 조작 종합 가이드
- `PR-vs-COMMIT-FAQ.md` - PR이 커밋으로 표시되는 이유

## 라이선스

이 프로젝트는 교육 목적입니다. 책임감 있고 윤리적으로 사용하세요.

## 작성자

[@devJZen](https://github.com/devJZen)

---

**최종 업데이트**: 2026-01-05

**핵심 통찰**: GitHub 잔디밭은 Git의 분산 신뢰 모델을 기반으로 합니다 - 클라이언트가 날짜를 설정하고, 서버는 검증 없이 저장합니다. 이것은 버그가 아니라 기능입니다! 🎨
