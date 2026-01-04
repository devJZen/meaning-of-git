# GitHub 잔디밭 대화형 에디터

키보드로 직접 GitHub 잔디밭 패턴을 그리고 실제 커밋으로 생성하는 도구

## 사용 워크플로우

```bash
# Step 1: 패턴 디자인
python3 github_canvas.py
# → 패턴을 그리고 S로 저장 (patterns/pattern.json)
# → Q로 종료

# Step 2: 커밋 생성
python3 git_generator.py generate pattern.json 2024
# → 실제 Git 커밋 생성

# Step 3: GitHub 푸시
cd ..
git push -f origin main
```

> **2단계 프로세스**: `github_canvas.py`는 패턴 **디자인**만, `git_generator.py`가 실제 **커밋 생성**

---

## 기능

- 터미널에서 대화형으로 패턴 그리기
- 실시간 미리보기
- 2가지 표시 스타일 (음영/블록) 전환
- 패턴 저장/불러오기 (JSON)
- Git 커밋 자동 생성
- 5단계 강도 조절

## 폴더 구조

```
interactive-cli/
├── github_canvas.py    # 대화형 에디터
├── git_generator.py    # Git 커밋 생성기
├── patterns/           # 패턴 저장 폴더 (자유롭게 추가/삭제 가능)
│   └── pattern.json    # 저장된 패턴 파일
└── README.md
```

**patterns 폴더**:

- 패턴 파일(.json)이 저장되는 폴더입니다
- 파일을 자유롭게 추가하거나 삭제할 수 있습니다
- 여러 패턴을 다른 이름으로 저장하여 관리할 수 있습니다

## 사용법

### 1. 대화형 에디터 실행

```bash
python3 github_canvas.py
```

### 2. 키 조작법

| 키               | 기능                              |
| ---------------- | --------------------------------- |
| ↑↓←→         | 커서 이동                         |
| Space            | 셀 강도 토글 (0→1→2→3→4→0)   |
| 0-4              | 직접 강도 설정                    |
| T                | 표시 스타일 변경 (음영 ↔ 블록)   |
| Delete/Backspace | 셀 지우기                         |
| S                | 패턴 저장 (patterns/pattern.json) |
| L                | 패턴 불러오기                     |
| C                | 캔버스 초기화                     |
| Q / ESC          | 종료 (저장 확인)                  |

### 표시 스타일

**음영 스타일** (기본):

- ⬜ ░░ ▒▒ ▓▓ ██
- 강도 차이가 명확하게 보입니다

**블록 스타일**:

- 배경색이 채워지는 기존 방식
- GitHub 잔디밭과 유사한 느낌

### 3. 패턴 미리보기

```bash
python3 git_generator.py preview pattern.json
```

### 4. Git 커밋 생성

```bash
python3 git_generator.py generate pattern.json
# 또는 특정 연도 지정
python3 git_generator.py generate pattern.json 2024
```

### 5. GitHub에 푸시

```bash
git push -f origin main
```

## 강도 레벨

- **0**: 비어있음 (커밋 없음)
- **1**: 연한 초록 (1-3개 커밋)
- **2**: 중간 초록 (4-7개 커밋)
- **3**: 진한 초록 (8-12개 커밋)
- **4**: 매우 진한 초록 (13-20개 커밋)

## 예제 워크플로우

1. 에디터를 열고 원하는 패턴을 그립니다
2. `T` 키로 스타일을 변경하며 미리 확인합니다
3. `S`를 눌러 `patterns/pattern.json`에 저장합니다
4. `Q`로 에디터를 종료합니다
5. `python3 git_generator.py generate pattern.json`로 커밋 생성
6. `git push -f origin main`으로 GitHub에 푸시

## 여러 패턴 관리

다른 이름으로 패턴을 저장하려면:

1. 에디터에서 패턴을 그립니다
2. 종료 후 `patterns/pattern.json`을 다른 이름으로 복사합니다
   ```bash
   cp patterns/pattern.json patterns/flower.json
   cp patterns/pattern.json patterns/heart.json
   ```
3. 원하는 패턴으로 커밋 생성:
   ```bash
   python3 git_generator.py generate flower.json 2024
   ```

## 패턴 파일 형식

패턴은 JSON 형식으로 `patterns/` 폴더에 저장됩니다:

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

## 주의사항

- `git push -f`는 기존 커밋 히스토리를 덮어씁니다
- 중요한 저장소에는 사용하지 마세요
- 패턴은 7줄(요일) x 52칸(주) 크기입니다
- `patterns/` 폴더의 파일은 자유롭게 추가/삭제 가능합니다
