# GPG 서명과 커밋 불변성 연구

> **연구 상태**: 문제 발견 및 분석 완료

Claude와 함께 작성했습니다.
수정일: 2026년 6월 15일

---

## 결론

날짜 조작이 아니라 Git의 기능이었으며 해당 프로젝트는 분산형 시스템의 초기모델 사용하고 확인하는 것이 좋다.
커밋의 날짜를 확실히 기록하고 싶으면 다른 형상 관리를 사용하면 된다.

## 개요

Git 커밋의 "불변성"이 실제로 무엇을 의미하는지, GPG 서명이 타임스탬프 변경을 막는지에 대한 실험적 연구.
두 가지 시나리오를 직접 실험하여 git graph가 어떻게 달라지는지 기록했다.

---

## Git 커밋 해시의 구조 (불변성의 실체)

Git은 커밋 오브젝트를 SHA-1로 해싱한 값을 커밋 해시로 사용한다.  
이 해시는 다음 데이터 전체를 포함한다:

```
commit <size>\0
tree <tree-hash>
parent <parent-hash>
author <name> <email> <unix-timestamp> <timezone>
committer <name> <email> <unix-timestamp> <timezone>
[gpgsig <PGP-signature>]    ← GPG 서명이 있으면 이 필드가 추가됨

<commit-message>
```

**핵심**: GPG 서명(`gpgsig`)은 커밋 오브젝트의 일부다.  
따라서 서명을 추가하면 같은 메시지/트리/날짜라도 **해시가 달라진다**.

---

## 실험 환경

- 연구용 GPG 키 생성 (passphrase 없음, `gpg-test@research.local`)
- Key ID: `DDD40EC5792A9AF0`
- 브랜치: `research/gpg-immutability`
- Git에 등록되지 않은 GPG로 커밋(Git에 등록된 GPG로 서명한 커밋을 작성하면 해당 날짜에 서명된 커밋이 기록된다.)

---

## 시나리오 A: 기존 커밋에 GPG 서명 소급 추가

### 실험 과정

1. 서명 없이 커밋 3개 생성 (커스텀 날짜 설정)
2. `git rebase -f --gpg-sign=<key>` 로 소급 서명

### Before: 서명 전 커밋 해시

```
d12803568e45595eb6692846b6f828d74416efa6  2026-01-10 09:00:00 UTC  [N]
cf44ed6d80c9f75987335bd70869c46b4cd58dd3  2026-02-14 12:00:00 UTC  [N]
32de4cae879c04d01c051589581331c4408cf207  2026-03-21 18:00:00 UTC  [N]
```

`[N]` = No signature

### After: 소급 서명 후 커밋 해시

```
c701b78a2e88077365b453d0d8a0be24a54ced3f  2026-01-10 09:00:00 UTC  [G]
1bef648abd7cbe46b513b5c7962e6e01e90bcc85  2026-02-14 12:00:00 UTC  [G]
3f617d75d8c72bd66085247ff83e0a73da7a5c4f  2026-03-21 18:00:00 UTC  [G]
```

`[G]` = Good signature

### 관찰 1: 해시가 완전히 교체됨

3개 커밋 모두 새로운 해시로 대체되었다. `d12803...` 오브젝트는 로컬 git DB에서 사라지지는 않지만, 브랜치 포인터는 새 해시를 가리킨다.

```
d128035  →  c701b78   (Jan-10 커밋)
cf44ed6  →  1bef648   (Feb-14 커밋)
32de4ca  →  3f617d7   (Mar-21 커밋)
```

이미 공유된 리포지토리(GitHub 등)에서는 이 변경이 force push 없이 반영 불가능하다.

### 관찰 2: Committer Date가 서명 시점으로 변경됨 ← 예상치 못한 발견

```
커밋 오브젝트 (c701b78) 내부:
  author    name <test@gmail.com>  1768035600 +0000   → 2026-01-10 (원본 날짜 유지)
  committer name <test@gmail.com>  1781307014 +0900   → 2026-06-13 (서명 수행 시점!)
```

`git rebase`는 커밋을 재생성하므로 `GIT_COMMITTER_DATE` 환경변수를 별도로 설정하지 않으면 committer date가 현재 시각으로 리셋된다. **서명을 소급 추가한 흔적이 committer date에 남는다.**

`git log --format="%ai / %ci"` 로 확인:

```
author_date   : 2026-01-10 09:00:00 +0000
committer_date: 2026-06-13 08:30:14 +0900   ← 오늘 날짜 (서명 시점)
```

---

## 시나리오 B: 처음부터 GPG 서명과 함께 타임스탬프 변경

### 실험 과정

`GIT_AUTHOR_DATE` 와 `GIT_COMMITTER_DATE` 를 설정한 뒤 `git commit -S` 로 서명 포함 커밋.

```bash
GIT_AUTHOR_DATE="2025-06-15 10:00:00 +0000" \
GIT_COMMITTER_DATE="2025-06-15 10:00:00 +0000" \
git commit -S -m "scenario-B: commit-1"
```

### 결과: 서명 유효 + 타임스탬프 완전 조작 가능

```
9242ded  GPG=G  author=2025-06-15 10:00:00  committer=2025-06-15 10:00:00  (backdated)
14729bf  GPG=G  author=2027-03-01 08:30:00  committer=2027-03-01 08:30:00  (future)
2f2f8d2  GPG=G  author=2024-11-05 23:59:59  committer=2024-11-05 23:59:59  (past)
```

세 커밋 모두 GPG 서명 상태가 `G` (유효)이면서 과거/미래/백데이트 타임스탬프를 가진다.  
`git verify-commit` 도 정상 통과한다.

커밋 오브젝트 내부 (9242ded):

```
tree 7fff277928c1ea0377f827c975cddcc6a9fee541
parent 3f617d75d8c72bd66085247ff83e0a73da7a5c4f
author name <test@gmail.com> 1749981600 +0000
committer name <test@gmail.com> 1749981600 +0000
gpgsig -----BEGIN PGP SIGNATURE-----
 
 iQEzBAABCAAdFiEES5LY23wxHTT2rIcB3dQOxXkqmvAFAmoslpYACgkQ...
 -----END PGP SIGNATURE-----

scenario-B: commit-1 (gpg+backdated, date=2025-Jun-15)
```

GPG 서명은 "이 내용(2025-06-15 타임스탬프 포함)을 `DDD40EC5792A9AF0` 키 보유자가 서명했다"를 보장하지만, **그 타임스탬프가 실제 서명 시각과 일치하는지는 보장하지 않는다**.

---

## Git Graph 비교

```
* 2f2f8d2  G  2024-11-05  scenario-B: commit-3 (gpg+past)
* 14729bf  G  2027-03-01  scenario-B: commit-2 (gpg+future)
* 9242ded  G  2025-06-15  scenario-B: commit-1 (gpg+backdated)
* 3f617d7  G  2026-03-21  scenario-A: commit-3 (retroactively signed)
* 1bef648  G  2026-02-14  scenario-A: commit-2 (retroactively signed)
* c701b78  G  2026-01-10  scenario-A: commit-1 (retroactively signed)
* 1594474  N  2026-01-05  (unsigned commit)
```

### Git graph만 보면 A와 B가 구분되지 않는다

`git log --graph` 나 `git log --format="%G?"` 로는 두 시나리오 모두 `G` (Good signature)로 표시된다. 단순히 "서명이 있다"는 사실만으로는 어떤 방식으로 서명됐는지 알 수 없다.

### 유일한 차이점: author date vs committer date

| 시나리오 | author_date | committer_date |
|----------|-------------|----------------|
| A (소급 서명) | 원본 날짜 유지 | **서명 수행 시점 (실제 날짜)** |
| B (처음부터 서명) | 설정한 날짜 | 설정한 날짜 (동일) |

```bash
# 두 시나리오를 구별할 수 있는 명령어
git log --format="%h  author=%ai  committer=%ci  gpg=%G?"
```

출력:
```
2f2f8d2  author=2024-11-05 23:59:59 +0000  committer=2024-11-05 23:59:59 +0000  gpg=G
14729bf  author=2027-03-01 08:30:00 +0000  committer=2027-03-01 08:30:00 +0000  gpg=G
9242ded  author=2025-06-15 10:00:00 +0000  committer=2025-06-15 10:00:00 +0000  gpg=G
3f617d7  author=2026-03-21 18:00:00 +0000  committer=2026-06-13 08:30:14 +0900  gpg=G  ← 불일치!
1bef648  author=2026-02-14 12:00:00 +0000  committer=2026-06-13 08:30:14 +0900  gpg=G  ← 불일치!
c701b78  author=2026-01-10 09:00:00 +0000  committer=2026-06-13 08:30:14 +0900  gpg=G  ← 불일치!
```

시나리오 A의 커밋들은 `author_date ≠ committer_date` 이고, committer date가 모두 동일한 시각(서명 rebase 수행 시점)을 가리킨다.

---

## 핵심 발견 요약

### 1. GPG 서명은 해시를 바꾼다

서명을 소급 추가하면 모든 후속 커밋의 해시가 연쇄적으로 변경된다(parent hash 포함 → cascade).  
이미 푸시된 리포지토리에 적용하려면 force push가 필요하고, 다른 사람의 체크아웃이 무효화된다.

### 2. 소급 서명은 committer date 흔적을 남긴다

`git rebase`로 서명을 추가하면 committer date가 rebase 수행 시점으로 업데이트된다.

### 3. GPG 서명은 타임스탬프의 진위를 증명하지 않는다

`git commit -S` 는 커밋 내용(타임스탬프 포함)을 서명하지만, 그 타임스탬프가 실제 서명 시각과 같은지는 검증하지 않는다.
서명 전에 `GIT_AUTHOR_DATE` 와 `GIT_COMMITTER_DATE` 를 임의의 값으로 설정하면, 서명 유효성(`G`)을 유지하면서 임의의 타임스탬프를 가진 커밋을 만들 수 있다.

### 4. git log 출력만으로는 판별 불가

`G` 표시만으로는 "처음부터 올바른 날짜로 서명된 커밋"인지 "날짜를 조작해서 서명한 커밋"인지 구분할 수 없다.

---

## 미확인 사항 / 열린 질문

- [ ] GitHub이 push 수신 시 커밋 타임스탬프와 push 시각의 불일치를 기록하는가?
- [ ] GPG 서명의 내장 타임스탬프(서명 오브젝트 자체의 creation time)와 커밋 타임스탬프를 비교하면 변경을 탐지할 수 있는가?
- [ ] `git commit -S` 로 생성된 서명 오브젝트에는 서명 수행 시각이 포함되는가? (`gpg --verify` 출력 확인 필요)
- [ ] Transparency log (Sigstore, Rekor 등)와 연계하면 타임스탬프를 외부에서 앵커링할 수 있는가?

---

## 재현 명령어

```bash
# 시나리오 A: 서명 없이 커밋 후 소급 서명
GIT_AUTHOR_DATE="2026-01-10 09:00:00 +0000" \
GIT_COMMITTER_DATE="2026-01-10 09:00:00 +0000" \
git commit -m "unsigned commit"

git rebase -f --gpg-sign=<KEY_ID> HEAD~1   # committer date가 현재 시각으로 바뀜

# 시나리오 B: 처음부터 GPG 서명 + 타임스탬프 변경
GIT_AUTHOR_DATE="2024-01-01 00:00:00 +0000" \
GIT_COMMITTER_DATE="2024-01-01 00:00:00 +0000" \
git commit -S -m "signed but backdated"   # 서명 유효, 타임스탬프 변경됨

# 비교
git log --format="%h  author=%ai  committer=%ci  gpg=%G?"
```

---

*연구 날짜: 2026-06-13*  
*브랜치: `research/gpg-immutability`*
