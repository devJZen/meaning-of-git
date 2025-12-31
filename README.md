# git-log-hack

GitHub 잔디밭은 Author Date를 기준으로 그려지므로 과거와 미래 전부 통제할 수 있다.

Author Date 와 Committer Date로 간단하게 구현했다.

- 로컬에서 커밋 생성: 날짜는 클라이언트에서 자유롭게 설정할 수 있다.
- GitHub(서버)는 받은 커밋의 날짜를 검증 없이 저장한다.
- 서버는 날짜의 진위를 검증하지 않고 있다.

따라서 GitHub, GitLab 기타 등등 모든 Git 플랫폼은 조작이 가능하다.

# Example

```
55fd317 - devJZen, 1년 전 : Flower commit 52
7e81ed7 - devJZen, 12달 전 : Flower commit 51
341ddee - devJZen, 1년 전 : Flower commit 50
b2c4066 - devJZen, 1년 전 : Flower commit 49
9af3713 - devJZen, 1년 전 : Flower commit 48
```
