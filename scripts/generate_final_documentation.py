from __future__ import annotations

import importlib.util
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader, simpleSplit
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "AI-BASED PLANT DISEASE DETECTION FINAL DOCUMENTATION.pdf"
LOGO = ROOT / "assets" / "Image18.png"
HERO_IMAGE = ROOT / "src" / "assets" / "hero-plant.jpg"

PAGE_WIDTH, PAGE_HEIGHT = A4
LEFT = 56
RIGHT = 56
TOP = PAGE_HEIGHT - 56
BOTTOM = 56
TEXT_WIDTH = PAGE_WIDTH - LEFT - RIGHT

PROJECT_TITLE = "AI-BASED PLANT DISEASE DETECTION"
FULL_TITLE = "AI-BASED PLANT DISEASE DETECTION"
AUTHOR = "SHUAIB AHMED"
REG_NO = "2313181033049"
GUIDE = "DR. M. MOHAMED SUHAIL"


def load_content_pages():
    module_path = ROOT / "scripts" / "generate_one_page_report.py"
    spec = importlib.util.spec_from_file_location("one_page_report", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    pages = module.build_pages()

    if len(pages) != 48:
        raise ValueError(f"Expected 48 content pages, got {len(pages)}")

    if pages[0][1] == "PROJECT SUMMARY" and pages[1][1] == "ABSTRACT":
        pages[0], pages[1] = pages[1], pages[0]
    return pages


def draw_page_number(c: canvas.Canvas, page_no: int) -> None:
    c.setFont("Helvetica", 9)
    c.drawRightString(PAGE_WIDTH - 48, 28, str(page_no))


def draw_border(c: canvas.Canvas) -> None:
    c.setLineWidth(1)
    c.rect(34, 34, PAGE_WIDTH - 68, PAGE_HEIGHT - 68)
    c.setLineWidth(0.5)
    c.rect(42, 42, PAGE_WIDTH - 84, PAGE_HEIGHT - 84)


def draw_header(c: canvas.Canvas, show_department: bool = True) -> None:
    draw_border(c)
    if LOGO.exists():
        logo_w = 74
        logo_h = 74
        logo_x = (PAGE_WIDTH - logo_w) / 2
        logo_y = PAGE_HEIGHT - 138
        c.drawImage(ImageReader(str(LOGO)), logo_x, logo_y, width=logo_w, height=logo_h, preserveAspectRatio=True, mask="auto")
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT - 48, "THE NEW COLLEGE")
    c.setFont("Helvetica", 9.4)
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT - 65, "(AN AUTONOMOUS INSTITUTION TO THE UNIVERSITY OF MADRAS)")
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT - 79, "(ACCREDITED BY NAAC WITH 'A++' GRADE OF 3.61/4 IN THE 4th CYCLE)")
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT - 93, "Sponsored by: THE MUSLIM EDUCATIONAL ASSOCIATION OF SOUTHERN INDIA (MEASI)")
    if show_department:
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT - 144, "Department of Computer Applications")


def draw_cover(c: canvas.Canvas) -> None:
    draw_header(c)
    y = PAGE_HEIGHT - 220
    c.setFont("Helvetica-Bold", 18)
    for line in simpleSplit(FULL_TITLE, "Helvetica-Bold", 18, 360):
        c.drawCentredString(PAGE_WIDTH / 2, y, line)
        y -= 24

    y -= 18
    c.setFont("Helvetica", 11)
    c.drawCentredString(PAGE_WIDTH / 2, y, "A dissertation submitted in partial fulfillment of the requirements")
    y -= 15
    c.drawCentredString(PAGE_WIDTH / 2, y, "for the award of degree")

    y -= 40
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(PAGE_WIDTH / 2, y, "BACHELOR OF COMPUTER APPLICATIONS")
    y -= 36

    c.setFont("Helvetica", 11)
    c.drawCentredString(PAGE_WIDTH / 2, y, "By")
    y -= 22
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(PAGE_WIDTH / 2, y, AUTHOR)
    y -= 18
    c.setFont("Helvetica", 11)
    c.drawCentredString(PAGE_WIDTH / 2, y, f"REG. NO: {REG_NO}")

    y -= 38
    c.setFont("Helvetica", 11)
    c.drawCentredString(PAGE_WIDTH / 2, y, "Under the Guidance of")
    y -= 22
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(PAGE_WIDTH / 2, y, GUIDE)
    y -= 16
    c.setFont("Helvetica", 10)
    c.drawCentredString(PAGE_WIDTH / 2, y, "Assistant Professor")

    c.setFont("Helvetica", 11)
    c.drawCentredString(PAGE_WIDTH / 2, 66, "2025 - 2026")
    c.showPage()


def draw_bonafide(c: canvas.Canvas) -> None:
    draw_header(c)
    y = PAGE_HEIGHT - 180
    c.setFont("Helvetica-Bold", 15)
    c.drawCentredString(PAGE_WIDTH / 2, y, "BONAFIDE CERTIFICATE")
    y -= 42

    paragraphs = [
        f"This is to certify that the project work entitled {PROJECT_TITLE} is a bonafide record work done by {AUTHOR}, Reg. No: {REG_NO}, in partial fulfillment of the requirement for the award of the Degree of Bachelor of Computer Applications.",
        f"The work has been carried out under the guidance of {GUIDE}, Assistant Professor, Department of Computer Applications, The New College, Chennai - 14.",
    ]
    c.setFont("Helvetica", 11)
    for para in paragraphs:
        for line in simpleSplit(para, "Helvetica", 11, TEXT_WIDTH):
            c.drawString(LEFT, y, line)
            y -= 16
        y -= 12

    y -= 70
    c.line(LEFT + 20, y, LEFT + 150, y)
    c.line(PAGE_WIDTH - RIGHT - 150, y, PAGE_WIDTH - RIGHT - 20, y)
    c.setFont("Helvetica", 10)
    c.drawCentredString(LEFT + 85, y - 14, "Project Guide")
    c.drawCentredString(PAGE_WIDTH - RIGHT - 85, y - 14, "Head of the Department")

    y -= 74
    c.setFont("Helvetica", 10.5)
    c.drawString(LEFT, y, "Submitted for the Viva Voce Examination held on __________________ at The New College, Chennai - 14")

    y -= 80
    c.line(LEFT + 20, y, LEFT + 150, y)
    c.line(PAGE_WIDTH - RIGHT - 150, y, PAGE_WIDTH - RIGHT - 20, y)
    c.setFont("Helvetica", 10)
    c.drawCentredString(LEFT + 85, y - 14, "Internal Examiner")
    c.drawCentredString(PAGE_WIDTH - RIGHT - 85, y - 14, "External Examiner")
    c.showPage()


def draw_acknowledgement(c: canvas.Canvas) -> None:
    draw_header(c, show_department=False)
    y = PAGE_HEIGHT - 160
    c.setFont("Helvetica-Bold", 15)
    c.drawCentredString(PAGE_WIDTH / 2, y, "ACKNOWLEDGEMENT")
    y -= 36
    c.setFont("Helvetica-Oblique", 11)
    c.drawCentredString(PAGE_WIDTH / 2, y, '"In the name of Allah, the most Beneficent, the most Merciful"')
    y -= 34

    paragraphs = [
        "I would like to express my sincere gratitude to the Principal of The New College, Chennai, for providing the facilities and academic environment necessary for the successful completion of this project.",
        "I extend my heartfelt thanks to the Head of the Department of Computer Applications for the encouragement, support, and guidance offered throughout the course of this work.",
        f"I am especially grateful to my project guide, {GUIDE}, Assistant Professor, Department of Computer Applications, for his valuable suggestions, consistent guidance, and timely support during the design, development, and documentation of this project.",
        "I also thank all faculty members, my family, and my friends for their encouragement and support, which greatly helped me in completing this project successfully.",
    ]
    c.setFont("Helvetica", 11)
    for para in paragraphs:
        for line in simpleSplit(para, "Helvetica", 11, TEXT_WIDTH):
            c.drawString(LEFT, y, line)
            y -= 16
        y -= 10

    c.setFont("Helvetica-Bold", 11)
    c.drawRightString(PAGE_WIDTH - RIGHT, 80, AUTHOR)
    c.showPage()


def draw_index(c: canvas.Canvas, content_pages) -> None:
    draw_header(c, show_department=False)
    y = PAGE_HEIGHT - 156
    c.setFont("Helvetica-Bold", 15)
    c.drawCentredString(PAGE_WIDTH / 2, y, "INDEX")
    y -= 28

    rows = [(i + 1, item[1], i + 5) for i, item in enumerate(content_pages)]
    c.setFont("Helvetica-Bold", 8.5)
    left_x = LEFT
    right_x = PAGE_WIDTH / 2 + 14
    c.drawString(left_x, y, "S. NO.")
    c.drawString(left_x + 38, y, "TITLE")
    c.drawString(left_x + 210, y, "PAGE")
    c.drawString(right_x, y, "S. NO.")
    c.drawString(right_x + 38, y, "TITLE")
    c.drawString(right_x + 210, y, "PAGE")
    y -= 16

    c.setFont("Helvetica", 6.9)
    half = (len(rows) + 1) // 2
    left_rows = rows[:half]
    right_rows = rows[half:]
    for idx in range(max(len(left_rows), len(right_rows))):
        row_y = y - idx * 16
        if idx < len(left_rows):
            s_no, title, page = left_rows[idx]
            c.drawString(left_x, row_y, str(s_no))
            short_title = title[:40] + "..." if len(title) > 43 else title
            c.drawString(left_x + 18, row_y, short_title)
            c.drawRightString(left_x + 240, row_y, str(page))
        if idx < len(right_rows):
            s_no, title, page = right_rows[idx]
            c.drawString(right_x, row_y, str(s_no))
            short_title = title[:40] + "..." if len(title) > 43 else title
            c.drawString(right_x + 18, row_y, short_title)
            c.drawRightString(right_x + 240, row_y, str(page))

    draw_page_number(c, 4)
    c.showPage()


def draw_text_page(c: canvas.Canvas, title: str, paragraphs: list[str], bullets: list[str], page_no: int) -> None:
    draw_border(c)
    y = TOP
    c.setFont("Helvetica-Bold", 15)
    c.drawString(LEFT, y, title)
    y -= 28

    blocks = []
    total_lines = 0
    for para in paragraphs:
        lines = simpleSplit(para, "Helvetica", 10.5, TEXT_WIDTH)
        blocks.append(("para", lines))
        total_lines += len(lines)
    for bullet in bullets:
        lines = simpleSplit(f"- {bullet}", "Helvetica", 10.5, TEXT_WIDTH)
        blocks.append(("bullet", lines))
        total_lines += len(lines)

    usable_height = y - BOTTOM - 18
    base_line_gap = 14
    block_gap_count = max(len(blocks) - 1, 1)
    base_height = total_lines * base_line_gap + block_gap_count * 10
    extra_space = max(0, usable_height - base_height)
    extra_line_gap = min(2.5, extra_space / max(total_lines, 1))
    extra_block_gap = min(12, extra_space / block_gap_count) if block_gap_count else 0

    c.setFont("Helvetica", 10.5)
    for index, (_, lines) in enumerate(blocks):
        for line in lines:
            c.drawString(LEFT, y, line)
            y -= base_line_gap + extra_line_gap
        if index != len(blocks) - 1:
            y -= 10 + extra_block_gap

    draw_page_number(c, page_no)
    c.showPage()


def draw_code_page(c: canvas.Canvas, title: str, code: str, page_no: int) -> None:
    draw_border(c)
    y = TOP
    c.setFont("Helvetica-Bold", 13.5)
    c.drawString(LEFT, y, title)
    y -= 24

    max_chars = 104
    raw_lines = [line[:max_chars] for line in code.splitlines()]
    usable_height = y - BOTTOM - 16
    line_gap = max(8.0, min(10.0, usable_height / max(len(raw_lines), 1)))

    c.setFont("Courier", 7.1)
    for line in raw_lines:
        c.drawString(LEFT, y, line)
        y -= line_gap
        if y < BOTTOM + 8:
            break

    draw_page_number(c, page_no)
    c.showPage()


def draw_placeholder_page(c: canvas.Canvas, title: str, page_no: int) -> None:
    draw_border(c)
    y = TOP
    c.setFont("Helvetica-Bold", 15)
    c.drawString(LEFT, y, title)
    y -= 34
    if HERO_IMAGE.exists():
        c.drawImage(ImageReader(str(HERO_IMAGE)), LEFT + 18, PAGE_HEIGHT / 2 - 80, width=PAGE_WIDTH - LEFT - RIGHT - 36, height=220, preserveAspectRatio=True, mask="auto")
    c.setFont("Helvetica", 10.5)
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT / 2 - 110, "Project interface presentation page")
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT / 2 - 128, "Included as part of the final documentation layout.")
    draw_page_number(c, page_no)
    c.showPage()


def main() -> None:
    content_pages = load_content_pages()
    c = canvas.Canvas(str(OUTPUT), pagesize=A4)

    draw_cover(c)
    draw_bonafide(c)
    draw_acknowledgement(c)
    draw_index(c, content_pages)

    for page_no, (kind, title, payload) in enumerate(content_pages, start=5):
        if kind == "title":
            draw_page_number(c, page_no)
            c.setFont("Helvetica-Bold", 18)
            c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT / 2 + 8, title)
            c.showPage()
        elif kind == "text":
            draw_text_page(c, title, payload["paragraphs"], payload["bullets"], page_no)
        elif kind == "code":
            draw_code_page(c, title, payload["code"], page_no)
        elif kind == "placeholder":
            draw_placeholder_page(c, title, page_no)

    c.save()
    print(OUTPUT)
    print(f"pages={4 + len(content_pages)}")


if __name__ == "__main__":
    main()
