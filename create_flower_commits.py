#!/usr/bin/env python3
"""
GitHub 잔디밭에 꽃(튤립) 패턴을 그리는 스크립트
2024년 달력에 여러 개의 튤립을 고르게 배치합니다.
"""

import subprocess
from datetime import datetime, timedelta
import random
import os

# 튤립 패턴 (7줄 x 5칸)
# 1 = 커밋 있음, 0 = 커밋 없음
TULIP_PATTERN = [
    [0, 0, 1, 0, 0],  # 일요일
    [0, 1, 1, 1, 0],  # 월요일
    [1, 1, 1, 1, 1],  # 화요일
    [0, 1, 1, 1, 0],  # 수요일
    [0, 0, 1, 0, 0],  # 목요일
    [0, 0, 1, 0, 0],  # 금요일
    [0, 0, 1, 0, 0],  # 토요일
]

# 2024년 1월 1일은 월요일입니다
# GitHub 잔디밭은 일요일부터 시작하므로 2023-12-31(일요일)부터 시작
START_DATE = datetime(2023, 12, 31)

# 튤립을 배치할 주 간격 (0부터 시작)
# 2024년은 약 52주이므로, 고르게 배치하기 위해 여러 위치에 배치
TULIP_START_WEEKS = [5, 14, 23, 32, 41, 50]  # 6개의 튤립

# 하루에 생성할 커밋 수 범위
COMMITS_PER_DAY = (5, 10)


def create_commit(date, commit_number):
    """특정 날짜에 커밋 생성"""
    # 커밋 시간을 랜덤하게 설정 (더 자연스럽게)
    hour = random.randint(9, 22)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    commit_date = date.replace(hour=hour, minute=minute, second=second)
    date_str = commit_date.strftime("%Y-%m-%d %H:%M:%S")

    # 더미 파일 생성/수정
    with open("flower_commits.txt", "a") as f:
        f.write(f"Commit on {date_str}\n")

    # git add
    subprocess.run(["git", "add", "flower_commits.txt"], check=True)

    # git commit with custom date
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str

    commit_message = f"Flower commit {commit_number}"
    subprocess.run(
        ["git", "commit", "-m", commit_message],
        env=env,
        check=True,
        capture_output=True
    )


def draw_tulip(start_week):
    """특정 주에 튤립 그리기"""
    commit_count = 0

    for week_offset in range(5):  # 튤립 너비 (5주)
        for day_of_week in range(7):  # 일요일(0) ~ 토요일(6)
            if TULIP_PATTERN[day_of_week][week_offset] == 1:
                # 해당 날짜 계산
                days_from_start = (start_week + week_offset) * 7 + day_of_week
                commit_date = START_DATE + timedelta(days=days_from_start)

                # 2024년 범위 내에 있는지 확인
                if datetime(2024, 1, 1) <= commit_date <= datetime(2024, 12, 31):
                    # 해당 날짜에 여러 개의 커밋 생성
                    num_commits = random.randint(*COMMITS_PER_DAY)
                    for i in range(num_commits):
                        commit_count += 1
                        create_commit(commit_date, commit_count)
                        print(f"✓ 커밋 생성: {commit_date.strftime('%Y-%m-%d')} (#{commit_count})")

    return commit_count


def main():
    print("=" * 60)
    print("🌷 GitHub 잔디밭 꽃 그리기 시작!")
    print("=" * 60)
    print()

    total_commits = 0

    # 여러 개의 튤립 그리기
    for idx, start_week in enumerate(TULIP_START_WEEKS, 1):
        print(f"\n🌷 튤립 #{idx} 그리는 중 (시작 주: {start_week})...")
        commits = draw_tulip(start_week)
        total_commits += commits
        print(f"   → {commits}개 커밋 생성 완료")

    print()
    print("=" * 60)
    print(f"✅ 완료! 총 {total_commits}개의 커밋이 생성되었습니다.")
    print("=" * 60)
    print()
    print("다음 명령어로 GitHub에 푸시하세요:")
    print("  git push -f origin main")
    print()
    print("⚠️  주의: 기존 리모트 저장소가 있다면 --force 옵션이 필요할 수 있습니다.")
    print()


if __name__ == "__main__":
    main()
