#!/usr/bin/env python3
"""
GitHub 잔디밭 대화형 에디터
키보드로 직접 그림을 그릴 수 있습니다.
"""

import curses
import json
import os
from datetime import datetime, timedelta
from typing import List, Tuple


class GitHubCanvas:
    """GitHub 잔디밭 캔버스"""

    def __init__(self):
        self.width = 52  # 52주
        self.height = 7  # 일요일~토요일
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.cursor_x = 0
        self.cursor_y = 0
        self.intensity_levels = [0, 1, 2, 3, 4]  # 0=없음, 1-4=강도
        self.current_intensity = 0

    def toggle_cell(self):
        """현재 셀의 강도 토글"""
        current = self.grid[self.cursor_y][self.cursor_x]
        # 순환: 0 -> 1 -> 2 -> 3 -> 4 -> 0
        self.grid[self.cursor_y][self.cursor_x] = (current + 1) % 5

    def clear_cell(self):
        """현재 셀 지우기"""
        self.grid[self.cursor_y][self.cursor_x] = 0

    def set_intensity(self, intensity):
        """현재 셀에 특정 강도 설정"""
        if 0 <= intensity <= 4:
            self.grid[self.cursor_y][self.cursor_x] = intensity

    def move_cursor(self, dy, dx):
        """커서 이동"""
        new_y = (self.cursor_y + dy) % self.height
        new_x = (self.cursor_x + dx) % self.width
        self.cursor_y = new_y
        self.cursor_x = new_x

    def save_pattern(self, filename):
        """패턴을 JSON 파일로 저장"""
        # patterns 폴더가 없으면 생성
        patterns_dir = 'patterns'
        if not os.path.exists(patterns_dir):
            os.makedirs(patterns_dir)

        filepath = os.path.join(patterns_dir, filename)
        data = {
            'grid': self.grid,
            'width': self.width,
            'height': self.height,
            'created': datetime.now().isoformat()
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def load_pattern(self, filename):
        """JSON 파일에서 패턴 불러오기"""
        filepath = os.path.join('patterns', filename)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                data = json.load(f)
                self.grid = data['grid']
                self.width = data['width']
                self.height = data['height']
                return True
        return False

    def clear_all(self):
        """전체 캔버스 초기화"""
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]


class GitHubCanvasEditor:
    """대화형 캔버스 에디터"""

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.canvas = GitHubCanvas()
        self.status_message = ""  # 상태 메시지 (동적)
        self.style_mode = "shade"  # "shade" 또는 "block"

        # 단축키 안내 (항상 표시)
        self.help_lines = [
            "방향키: 이동 | Space: 색칠 | 숫자 0-4: 강도 | T: 스타일 변경",
            "S: 저장 | L: 불러오기 | C: 초기화 | Q/ESC: 종료"
        ]

        # 색상 초기화
        curses.start_color()
        curses.use_default_colors()

        # 음영 스타일용 색상 (전경색만, 배경 투명)
        curses.init_pair(1, curses.COLOR_WHITE, -1)    # 0: 비어있음 (흰색)
        curses.init_pair(2, curses.COLOR_GREEN, -1)    # 1: 연한 초록
        curses.init_pair(3, curses.COLOR_GREEN, -1)    # 2: 중간 초록
        curses.init_pair(4, curses.COLOR_GREEN, -1)    # 3: 진한 초록
        curses.init_pair(5, curses.COLOR_GREEN, -1)    # 4: 매우 진한 초록
        curses.init_pair(6, curses.COLOR_YELLOW, -1)   # 커서

        # 블록 스타일용 색상 (전경색=배경색)
        curses.init_pair(11, curses.COLOR_BLACK, curses.COLOR_BLACK)   # 0: 비어있음
        curses.init_pair(12, curses.COLOR_GREEN, curses.COLOR_GREEN)   # 1-4: 초록
        curses.init_pair(16, curses.COLOR_YELLOW, curses.COLOR_YELLOW) # 커서

        # 강도별 표시 문자
        self.shade_chars = ['⬜', '░░', '▒▒', '▓▓', '██']
        self.block_chars = ['  ', '██', '██', '██', '██']

        # 커서 숨기기
        curses.curs_set(0)

    def get_color_pair(self, intensity, is_cursor=False):
        """강도에 따른 색상 페어와 속성 반환"""
        if self.style_mode == "shade":
            # 음영 스타일
            if is_cursor:
                return curses.color_pair(6) | curses.A_REVERSE | curses.A_BOLD
            if intensity == 0:
                return curses.color_pair(1)  # 흰색 (비어있음)
            elif intensity == 1:
                return curses.color_pair(2) | curses.A_DIM  # 연한 초록
            elif intensity == 2:
                return curses.color_pair(3)  # 중간 초록
            elif intensity == 3:
                return curses.color_pair(4) | curses.A_BOLD  # 진한 초록
            else:  # intensity == 4
                return curses.color_pair(5) | curses.A_BOLD  # 매우 진한 초록
        else:
            # 블록 스타일 (기존)
            if is_cursor:
                return curses.color_pair(16)
            if intensity == 0:
                return curses.color_pair(11)  # 검정 (비어있음)
            elif intensity == 1:
                return curses.color_pair(12) | curses.A_DIM  # 연한 초록
            elif intensity == 2:
                return curses.color_pair(12)  # 중간 초록
            elif intensity == 3:
                return curses.color_pair(12) | curses.A_BOLD  # 진한 초록
            else:  # intensity == 4
                return curses.color_pair(12) | curses.A_BOLD  # 매우 진한 초록

    def get_display_char(self, intensity):
        """강도에 따른 표시 문자 반환"""
        if self.style_mode == "shade":
            return self.shade_chars[intensity]
        else:
            return self.block_chars[intensity]

    def toggle_style(self):
        """스타일 토글"""
        if self.style_mode == "shade":
            self.style_mode = "block"
            self.status_message = "✓ 블록 스타일로 변경"
        else:
            self.style_mode = "shade"
            self.status_message = "✓ 음영 스타일로 변경"

    def draw_canvas(self):
        """캔버스 그리기"""
        self.stdscr.clear()

        # 제목
        title = "🌷 GitHub 잔디밭 에디터"
        self.stdscr.addstr(0, 2, title, curses.A_BOLD)

        # 캔버스 그리기
        start_y = 2
        start_x = 2
        cell_width = 2

        for y in range(self.canvas.height):
            for x in range(self.canvas.width):
                intensity = self.canvas.grid[y][x]
                is_cursor = (y == self.canvas.cursor_y and x == self.canvas.cursor_x)

                color = self.get_color_pair(intensity, is_cursor)
                char = self.get_display_char(intensity)

                # 커서 위치 표시 (음영 스타일만)
                if is_cursor and self.style_mode == "shade":
                    char = "◆◆"  # 커서 전용 문자

                py = start_y + y
                px = start_x + x * cell_width

                try:
                    self.stdscr.addstr(py, px, char, color)
                except curses.error:
                    pass

        # 요일 라벨
        days = ['일', '월', '화', '수', '목', '금', '토']
        for i, day in enumerate(days):
            try:
                self.stdscr.addstr(start_y + i, start_x + self.canvas.width * cell_width + 2, day)
            except curses.error:
                pass

        # 현재 위치 정보
        info_y = start_y + self.canvas.height + 2
        info = f"위치: ({self.canvas.cursor_x}, {self.canvas.cursor_y}) | 현재 강도: {self.canvas.grid[self.canvas.cursor_y][self.canvas.cursor_x]}"
        self.stdscr.addstr(info_y, start_x, info)

        # 강도 범례 및 스타일 표시
        legend_y = info_y + 1
        style_name = "음영" if self.style_mode == "shade" else "블록"
        self.stdscr.addstr(legend_y, start_x, f"강도 (스타일: {style_name}): ")
        legend_offset = len(f"강도 (스타일: {style_name}): ")
        for i in range(5):
            color = self.get_color_pair(i)
            char = self.get_display_char(i)
            self.stdscr.addstr(legend_y, start_x + legend_offset + i * 4, char, color)
            self.stdscr.addstr(legend_y, start_x + legend_offset + 2 + i * 4, f"{i} ")

        # 단축키 안내 (항상 표시)
        help_y = legend_y + 2
        for i, help_line in enumerate(self.help_lines):
            try:
                self.stdscr.addstr(help_y + i, start_x, help_line, curses.A_DIM)
            except curses.error:
                pass

        # 상태 메시지 (동적 - 명령 실행 결과)
        if self.status_message:
            status_y = help_y + len(self.help_lines) + 1
            try:
                self.stdscr.addstr(status_y, start_x, f"[상태] {self.status_message}", curses.A_BOLD)
            except curses.error:
                pass

        self.stdscr.refresh()

    def run(self):
        """에디터 실행"""
        while True:
            self.draw_canvas()

            try:
                key = self.stdscr.getch()
            except KeyboardInterrupt:
                break

            # 방향키
            if key == curses.KEY_UP:
                self.canvas.move_cursor(-1, 0)
                self.status_message = ""  # 상태 메시지 지우기
            elif key == curses.KEY_DOWN:
                self.canvas.move_cursor(1, 0)
                self.status_message = ""
            elif key == curses.KEY_LEFT:
                self.canvas.move_cursor(0, -1)
                self.status_message = ""
            elif key == curses.KEY_RIGHT:
                self.canvas.move_cursor(0, 1)
                self.status_message = ""

            # 스페이스: 토글
            elif key == ord(' '):
                self.canvas.toggle_cell()
                self.status_message = ""

            # 숫자 0-4: 강도 설정
            elif key in [ord('0'), ord('1'), ord('2'), ord('3'), ord('4')]:
                intensity = int(chr(key))
                self.canvas.set_intensity(intensity)
                self.status_message = ""

            # Delete/Backspace: 셀 지우기
            elif key in [curses.KEY_BACKSPACE, curses.KEY_DC, 127]:
                self.canvas.clear_cell()
                self.status_message = ""

            # T: 스타일 토글
            elif key in [ord('t'), ord('T')]:
                self.toggle_style()

            # S: 저장
            elif key in [ord('s'), ord('S')]:
                self.canvas.save_pattern('pattern.json')
                self.status_message = "✓ 저장 완료: patterns/pattern.json"

            # L: 불러오기
            elif key in [ord('l'), ord('L')]:
                if self.canvas.load_pattern('pattern.json'):
                    self.status_message = "✓ 불러오기 완료: patterns/pattern.json"
                else:
                    self.status_message = "✗ patterns/pattern.json 파일을 찾을 수 없습니다"

            # C: 초기화
            elif key in [ord('c'), ord('C')]:
                self.canvas.clear_all()
                self.status_message = "✓ 캔버스 초기화 완료"

            # G: Git 커밋 생성
            elif key in [ord('g'), ord('G')]:
                self.status_message = "Git 커밋 생성 준비 중... (구현 예정)"

            # Q 또는 ESC: 종료
            elif key in [ord('q'), ord('Q'), 27]:
                # 저장 확인
                self.status_message = "저장하고 종료하시겠습니까? (y: 저장 후 종료 | n: 저장 안 함 | 기타: 취소)"
                self.draw_canvas()
                confirm = self.stdscr.getch()
                if confirm in [ord('y'), ord('Y')]:
                    self.canvas.save_pattern('pattern.json')
                    self.status_message = "✓ 저장 완료 (patterns/pattern.json). 종료합니다."
                    self.draw_canvas()
                    break
                elif confirm in [ord('n'), ord('N')]:
                    break
                else:
                    self.status_message = "종료를 취소했습니다."


def main(stdscr):
    """메인 함수"""
    editor = GitHubCanvasEditor(stdscr)
    editor.run()


if __name__ == "__main__":
    curses.wrapper(main)
