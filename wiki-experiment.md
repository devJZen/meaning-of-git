# Wiki 날짜 조작 실험 결과

## 실험 개요

**목적**: Wiki 커밋 날짜를 조작할 수 있는지, 잔디밭에 반영되는지 확인

**실험 날짜**: 2024-12-31
**테스트 커밋 날짜**: 2024-03-15 14:00:00

## 실험 과정

### 1단계: Wiki 활성화
- GitHub Settings → Features → Wikis 활성화
- 첫 Wiki 페이지 생성 (Home.md)

### 2단계: Wiki 리포지토리 클론
```bash
git clone https://github.com/devJZen/git-log-hack.wiki.git
cd git-log-hack.wiki
```

### 3단계: 과거 날짜로 페이지 생성
```bash
# Test-Date-Manipulation.md 생성
cat > Test-Date-Manipulation.md << 'EOF'
# Wiki Date Manipulation Test
...
EOF

# 과거 날짜로 커밋
git add Test-Date-Manipulation.md
GIT_AUTHOR_DATE="2024-03-15 14:00:00" \
GIT_COMMITTER_DATE="2024-03-15 14:00:00" \
git commit -m "Test: Wiki date manipulation (March 15, 2024)"
```

### 4단계: 푸시
```bash
git push origin master
```

## 실험 결과

### ✅ Git 로그 확인
```bash
$ git log --format="%h - %ai - %s"
124caa3 - 2024-03-15 14:00:00 +0900 - Test: Wiki date manipulation (March 15, 2024)
18af42b - 2025-12-31 22:34:23 +0900 - Initial Home page
```

**결과**: ✅ 과거 날짜로 커밋 생성 성공!

### GitHub 확인 사항

**1. Wiki 페이지 확인**:
- URL: https://github.com/devJZen/git-log-hack/wiki/Test-Date-Manipulation
- 페이지가 생성되었는지 확인

**2. Wiki 히스토리 확인**:
- Wiki 페이지 하단 "Page History" 클릭
- 커밋 날짜가 **2024-03-15**로 표시되는지 확인

**3. 잔디밭 확인** (가장 중요!):
- URL: https://github.com/devJZen
- 2024년 3월 15일에 초록색 표시되는지 확인

## 예상 결과

**가능성 1: 잔디밭 반영 O** ✅
- Wiki도 Git 리포지토리이므로 커밋으로 인정
- 2024년 3월 15일에 초록색 표시됨
- **Wiki 날짜 조작 완전히 작동!**

**가능성 2: 잔디밭 반영 X** ❌
- Wiki는 별도 리포지토리로 취급
- 메인 리포지토리 커밋만 잔디밭 반영
- **Wiki 날짜 조작은 가능하지만 잔디밭에는 무관**

## 실제 확인 결과

### Wiki 페이지
- [x] ✅ 페이지 생성 확인됨
- [x] ✅ 커밋 날짜 **March 15, 2024**로 완벽하게 표시됨
  - GitHub 표시: "@devJZen devJZen committed on Mar 15, 2024"

### 잔디밭
- [ ] 2024년 3월 15일에 초록색 표시됨 → 완전 성공!
- [x] ❌ **잔디밭 변화 없음** → 날짜 조작만 가능, 잔디밭 무관

## 최종 결론

### ✅ Wiki 날짜 조작: 성공!

**성공한 것**:
- Wiki 커밋 날짜를 과거(2024-03-15)로 조작 가능
- GitHub Wiki 히스토리에 조작된 날짜로 완벽하게 표시됨
- Git 리포지토리이므로 일반 커밋과 동일하게 작동

**제한사항**:
- ❌ Wiki 커밋은 GitHub 잔디밭에 반영되지 않음
- Wiki는 별도 리포지토리로 취급되어 기여도에 포함 안 됨

### 실용성 평가

**Wiki 날짜 조작의 용도**:
- ✅ Wiki 히스토리를 과거로 조작 가능
- ✅ 문서 작성 시점을 소급 적용 가능
- ❌ 잔디밭/기여도에는 무의미

**본 프로젝트 목적에는**:
- 잔디밭 패턴 그리기가 목표이므로 Wiki는 **사용 불가**
- 메인 리포지토리 커밋만 잔디밭에 반영됨

---

**실험 완료 시각**: 2024-12-31 22:36
**Wiki URL**: https://github.com/devJZen/git-log-hack/wiki
