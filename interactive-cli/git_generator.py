#!/usr/bin/env python3
"""
GitHub 잔디밭 패턴을 실제 Git 커밋으로 변환
"""

import subprocess
import os
import random
from datetime import datetime, timedelta
import json


class GitCommitGenerator:
    """Git 커밋 생성기"""

    def __init__(self, year=2024):
        self.year = year
        # 해당 연도의 첫 일요일 찾기
        jan_1 = datetime(year, 1, 1)
        # 1월 1일이 무슨 요일인지 확인 (0=월요일, 6=일요일)
        weekday = jan_1.weekday()
        # 첫 일요일까지의 일수 계산
        days_to_sunday = (6 - weekday) % 7
        if days_to_sunday == 0 and weekday != 6:
            days_to_sunday = -1
        self.start_date = jan_1 - timedelta(days=(weekday + 1) % 7)

    def intensity_to_commits(self, intensity):
        """강도를 커밋 개수로 변환"""
        if intensity == 0:
            return 0
        elif intensity == 1:
            return random.randint(1, 3)
        elif intensity == 2:
            return random.randint(4, 7)
        elif intensity == 3:
            return random.randint(8, 12)
        else:  # intensity == 4
            return random.randint(13, 20)

    def create_commit(self, date, commit_number):
        """특정 날짜에 커밋 생성"""
        # 커밋 시간을 랜덤하게 설정
        hour = random.randint(9, 22)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)

        commit_date = date.replace(hour=hour, minute=minute, second=second)
        date_str = commit_date.strftime("%Y-%m-%d %H:%M:%S")

        # 더미 파일 생성/수정
        commit_file = "canvas_commits.txt"
        with open(commit_file, "a") as f:
            f.write(f"Commit on {date_str}\n")

        # git add
        subprocess.run(["git", "add", commit_file], check=True)

        # git commit with custom date
        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"] = date_str
        env["GIT_COMMITTER_DATE"] = date_str

        commit_message = f"Canvas commit {commit_number}"
        subprocess.run(
            ["git", "commit", "-m", commit_message],
            env=env,
            check=True,
            capture_output=True
        )

        return date_str

    def generate_from_pattern(self, pattern_file):
        """패턴 파일에서 커밋 생성"""
        # 패턴 로드
        with open(pattern_file, 'r') as f:
            data = json.load(f)

        grid = data['grid']
        height = len(grid)
        width = len(grid[0]) if height > 0 else 0

        print("=" * 60)
        print("🎨 GitHub 잔디밭 커밋 생성 시작!")
        print("=" * 60)
        print(f"패턴 크기: {width}주 x {height}일")
        print(f"대상 연도: {self.year}")
        print()

        total_commits = 0
        dates_with_commits = []

        # 그리드를 순회하며 커밋 생성
        for week in range(width):
            for day in range(height):
                intensity = grid[day][week]

                if intensity > 0:
                    # 해당 날짜 계산
                    days_from_start = week * 7 + day
                    commit_date = self.start_date + timedelta(days=days_from_start)

                    # 연도 범위 확인
                    if commit_date.year != self.year:
                        continue

                    # 강도에 따라 커밋 개수 결정
                    num_commits = self.intensity_to_commits(intensity)

                    for i in range(num_commits):
                        total_commits += 1
                        date_str = self.create_commit(commit_date, total_commits)
                        print(f"✓ 커밋 생성: {date_str} (강도: {intensity}, #{total_commits})")

                    dates_with_commits.append(commit_date.strftime("%Y-%m-%d"))

        print()
        print("=" * 60)
        print(f"✅ 완료! 총 {total_commits}개의 커밋이 생성되었습니다.")
        print(f"📅 커밋이 생성된 날짜: {len(dates_with_commits)}일")
        print("=" * 60)
        print()
        print("다음 명령어로 GitHub에 푸시하세요:")
        print("  git push -f origin main")
        print()

        return total_commits

    def preview_pattern(self, pattern_file):
        """패턴 미리보기 (터미널)"""
        with open(pattern_file, 'r') as f:
            data = json.load(f)

        grid = data['grid']
        height = len(grid)
        width = len(grid[0]) if height > 0 else 0

        print("\n" + "=" * 60)
        print("🎨 패턴 미리보기")
        print("=" * 60)

        # 강도별 아이콘
        icons = ['⬜', '🟩', '🟩', '🟩', '🟩']
        shades = ['  ', '░░', '▒▒', '▓▓', '██']

        for day in range(height):
            for week in range(width):
                intensity = grid[day][week]
                print(shades[intensity], end='')
            print()

        print("=" * 60)
        print(f"크기: {width}주 x {height}일")
        print("=" * 60 + "\n")


def main():
    """메인 함수"""
    import sys

    if len(sys.argv) < 2:
        print("사용법:")
        print("  python git_generator.py preview pattern.json  # 미리보기")
        print("  python git_generator.py generate pattern.json  # 커밋 생성")
        print("  python git_generator.py generate pattern.json 2024  # 특정 연도")
        print()
        print("패턴 파일은 patterns/ 폴더에서 찾습니다.")
        return

    command = sys.argv[1]
    pattern_filename = sys.argv[2] if len(sys.argv) > 2 else "pattern.json"
    year = int(sys.argv[3]) if len(sys.argv) > 3 else 2024

    # patterns 폴더에서 파일 찾기
    pattern_file = os.path.join('patterns', pattern_filename)

    if not os.path.exists(pattern_file):
        print(f"✗ 오류: {pattern_file} 파일을 찾을 수 없습니다.")
        print(f"patterns/ 폴더에 패턴 파일이 있는지 확인하세요.")
        return

    generator = GitCommitGenerator(year)

    if command == "preview":
        generator.preview_pattern(pattern_file)
    elif command == "generate":
        generator.preview_pattern(pattern_file)
        print("위 패턴으로 커밋을 생성하시겠습니까? (y/n): ", end='')
        confirm = input().strip().lower()
        if confirm == 'y':
            generator.generate_from_pattern(pattern_file)
    else:
        print(f"알 수 없는 명령어: {command}")


if __name__ == "__main__":
    main()
