#!/usr/bin/env python3
"""Figures and posters of Digital Skills Unit 3 (week-03), drawn with svgkit.

    python3 plans/helpers/figs_u3.py && python3 plans/helpers/export_png.py <the SVGs>
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import (Svg, INK, MUTED, LINE, ORANGE, PEACH, SOFT, GREEN, GREEN_SOFT, RED, RED_SOFT,
                    BLUE, BLUE_SOFT, WORD, GREY_BG)

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W3 = os.path.join(ROOT, "courses", "digital-skills", "week-03")


def poster_head(s, title, hint, task=None, y_task=70):
    s.text(24, 34, title, size=21, weight=800)
    s.text(24, 56, hint, size=12, fill=MUTED)
    if task:
        s.rect(24, y_task, s.w - 48, 32, rx=10, fill=SOFT, stroke=PEACH, dash="6 4")
        s.text(36, y_task + 21, task, size=12.5, weight=800)


def button(s, x, y, w, label, on=False, h=26, size=12):
    s.rect(x, y, w, h, rx=8, fill=(BLUE if on else "#ffffff"), stroke=(BLUE if on else ORANGE), sw=1.5)
    s.text(x + w / 2, y + h / 2 + 4.5, label, size=size, fill=("#ffffff" if on else ORANGE), anchor="middle", weight=800)


def email_parts():
    s = Svg(700, 330)
    s.rect(20, 14, 420, 300, rx=12, fill="#ffffff", stroke=LINE)
    s.rect(20, 14, 420, 34, rx=12, fill=GREY_BG, stroke=None)
    s.rect(34, 22, 64, 20, rx=6, fill=BLUE, stroke=None)
    s.text(66, 36, "Send", size=11.5, fill="#ffffff", anchor="middle", weight=800)
    s.clip(116, 30, c=INK)
    s.text(130, 36, "Attach", size=11.5, weight=700)
    rows = [("To", "Omar; Lina", 74), ("Cc", "Mr Yousef", 104), ("Subject", "Agenda: staff meeting on Sunday", 134)]
    for lab, val, y in rows:
        s.text(36, y, lab, size=12, fill=MUTED, weight=700)
        s.text(100, y, val, size=12.5, weight=800)
        s.line(34, y + 10, 426, y + 10, stroke="#e9ecef", sw=1.2)
    s.rect(36, 152, 170, 30, rx=6, fill="#f8f9fa", stroke=LINE)
    s.doc(44, 157, w=16, h=20, c=WORD, rows=0)
    s.text(68, 172, "agenda.docx", size=11.5, weight=800)
    s.text(150, 172, "18 KB", size=10.5, fill=MUTED)
    s.lines(36, 208, ["Dear colleagues,", "here is the agenda of our meeting on Sunday.", "Please add your points.", "Huda"], size=12, weight=600, gap=19)
    labels = [(1, 74, "To: they read and act"), (2, 104, "Cc: they only need to know"),
              (3, 134, "Subject: what it is about"), (4, 167, "Attachment: the file"), (5, 32, "Send")]
    for n, y, t in labels:
        s.badge(458, y - 4, n)
        s.text(476, y, t if n != 5 else "Send", size=11.5, weight=800 if n != 5 else 800)
    s.text(458, 220, "Reply: back to the sender", size=11.5, fill=MUTED, weight=700)
    s.text(458, 240, "Reply all: to everyone", size=11.5, fill=MUTED, weight=700)
    s.text(458, 260, "Forward: to a new person,", size=11.5, fill=MUTED, weight=700)
    s.text(458, 278, "with the file", size=11.5, fill=MUTED, weight=700)
    s.save(os.path.join(W3, "images", "email-parts.svg"))


def meeting_invite():
    s = Svg(640, 310)
    s.rect(20, 14, 380, 282, rx=12, fill="#ffffff", stroke=LINE)
    s.rect(20, 14, 6, 282, rx=3, fill=ORANGE, stroke=None)
    s.text(42, 46, "Staff meeting", size=18, weight=800)
    s.text(42, 72, "Sunday, 11:00 to 12:00", size=12.5, weight=700)
    s.text(42, 94, "Room 21 and online", size=12.5, fill=MUTED, weight=700)
    s.rect(42, 108, 150, 32, rx=8, fill=BLUE, stroke=None)
    s.text(117, 129, "Join the meeting", size=12.5, fill="#ffffff", anchor="middle", weight=800)
    s.text(204, 129, "teams link", size=11, fill=MUTED, weight=600)
    s.text(42, 166, "Attendees", size=12, fill=MUTED, weight=700)
    for i, (n, st, c) in enumerate([("Omar", "Accepted", GREEN), ("Lina", "Tentative", "#e67700"), ("Sami", "Declined", RED)]):
        x = 42 + i * 118
        s.person(x + 10, 192, c=c, r=9)
        s.text(x + 26, 190, n, size=12, weight=800)
        s.text(x + 26, 206, st, size=10.5, fill=c, weight=800)
    for i, (lab, c) in enumerate([("Accept", GREEN), ("Tentative", "#e67700"), ("Decline", RED)]):
        x = 42 + i * 112
        s.rect(x, 236, 100, 30, rx=8, fill="#ffffff", stroke=c, sw=1.8)
        s.text(x + 50, 256, lab, size=12, fill=c, anchor="middle", weight=800)
    labels = [(1, 46, "Title"), (2, 72, "Date and time"), (3, 124, "Online meeting link"),
              (4, 192, "Attendees and their answers"), (5, 251, "The three answers")]
    for n, y, t in labels:
        s.badge(420, y - 4, n)
        s.text(438, y, t, size=12, weight=800)
    s.save(os.path.join(W3, "images", "meeting-invite.svg"))


def co_editing():
    s = Svg(640, 320)
    # cloud and the one file
    s.rect(20, 14, 380, 292, rx=12, fill="#ffffff", stroke=LINE)
    s.rect(20, 14, 380, 34, rx=12, fill=GREY_BG, stroke=None)
    s.text(36, 36, "meeting-report.docx · OneDrive", size=12, weight=800)
    s.rect(300, 21, 88, 20, rx=10, fill=GREEN_SOFT, stroke=GREEN, sw=1.2)
    s.text(344, 35, "AutoSave On", size=10.5, fill=GREEN, anchor="middle", weight=800)
    s.text(40, 76, "Report: staff meeting, Sunday", size=13, weight=800)
    s.bar(40, 92, 230, rows=2, gap=14)
    # Omar's cursor
    s.rect(40, 126, 120, 8, rx=2, fill="#d0ebff", stroke=None)
    s.line(160, 120, 160, 140, stroke=BLUE, sw=2)
    s.rect(160, 108, 40, 14, rx=4, fill=BLUE, stroke=None)
    s.text(180, 119, "Omar", size=9.5, fill="#ffffff", anchor="middle", weight=800)
    s.bar(40, 152, 250, rows=2, gap=14)
    # Lina's cursor
    s.line(126, 182, 126, 204, stroke=GREEN, sw=2)
    s.rect(126, 168, 36, 14, rx=4, fill=GREEN, stroke=None)
    s.text(144, 179, "Lina", size=9.5, fill="#ffffff", anchor="middle", weight=800)
    s.rect(38, 185, 84, 18, rx=2, fill="#fff3bf", stroke=None)
    s.text(40, 198, "Sales: 120 JD", size=12, weight=700)
    s.bar(40, 216, 220, rows=2, gap=14)
    # comment
    s.rect(292, 168, 98, 64, rx=8, fill="#fff9db", stroke="#fcc419", sw=1.4)
    s.text(300, 186, "Lina", size=10.5, weight=800)
    s.text(300, 202, "@Omar, is it", size=10.5, weight=700)
    s.text(300, 216, "120 or 150?", size=10.5, weight=700)
    s.line(130, 194, 292, 194, stroke="#fcc419", sw=1.2, dash="4 3")
    # version history
    s.rect(420, 14, 200, 292, rx=12, fill="#ffffff", stroke=LINE)
    s.text(436, 40, "Version History", size=13, weight=800)
    for i, (when, who) in enumerate([("Today 10:42", "Omar"), ("Today 9:15", "Lina"), ("Yesterday 18:30", "Huda"), ("Yesterday 11:05", "Mona")]):
        y = 60 + i * 52
        s.rect(432, y, 176, 42, rx=8, fill=(SOFT if i == 2 else "#ffffff"), stroke=(PEACH if i == 2 else LINE))
        s.text(444, y + 18, when, size=11.5, weight=800)
        s.text(444, y + 33, who, size=10.5, fill=MUTED, weight=700)
    s.rect(500, 270, 100, 26, rx=8, fill=ORANGE, stroke=None)
    s.text(550, 288, "Restore", size=12, fill="#ffffff", anchor="middle", weight=800)
    s.badge(214, 115, 1)
    s.badge(380, 160, 2)
    s.badge(600, 40, 3)
    s.text(36, 258, "1  Two people change the same file at the same time.", size=11.5, weight=700)
    s.text(36, 276, "2  A comment with @Omar tells Omar.", size=11.5, weight=700)
    s.text(36, 294, "3  Version History brings back an older version.", size=11.5, weight=700)
    s.save(os.path.join(W3, "images", "co-editing.svg"))


def poster_mail_lab():
    s = Svg(640, 400)
    poster_head(s, "Mail Lab: To, Cc, subject and file", "Send each e-mail right: To and Cc, a clear subject and the right file.",
                "Task 1 of 5: Huda sends the agenda. Mr Yousef only needs to know.")
    s.rect(24, 114, 470, 270, rx=14, fill="#ffffff", stroke=LINE)
    s.text(40, 140, "New mail", size=14, weight=800)
    for i, (n, on) in enumerate([("Omar", 2), ("Lina", 2), ("Mr Yousef", 2), ("Sami", 2)]):
        y = 156 + i * 34
        s.text(40, y + 18, n, size=12.5, weight=800)
        for k, lab in enumerate(["To", "Cc", "not in it"]):
            w = 40 if k < 2 else 74
            x = 140 + [0, 46, 92][k]
            button(s, x, y, w, lab, on=(k == on))
    s.text(40, 316, "Subject", size=12.5, weight=800)
    s.rect(110, 300, 260, 26, rx=8, fill="#f1f3f5", stroke=LINE)
    s.text(120, 318, "choose ...", size=12, fill=MUTED, weight=700)
    s.text(40, 352, "Attach", size=12.5, weight=800)
    s.rect(110, 336, 160, 26, rx=8, fill="#f1f3f5", stroke=LINE)
    s.text(120, 354, "choose a file ...", size=12, fill=MUTED, weight=700)
    s.rect(300, 336, 70, 30, rx=10, fill=ORANGE, stroke=None)
    s.text(335, 356, "Send", size=13, fill="#ffffff", anchor="middle", weight=800)
    s.save(os.path.join(W3, "sims", "mail-lab.svg"))


def poster_meeting_planner():
    s = Svg(640, 330)
    poster_head(s, "Meeting Planner: a time for everybody", "Green is free, red is busy. Tap the first hour when all three are free.",
                "Sunday: find one hour for Huda, Omar and Lina.")
    hours = [8, 9, 10, 11, 12, 13]
    busy = {"Huda": [8, 12], "Omar": [9], "Lina": [10, 13]}
    x0, cw = 110, 84
    for i, h in enumerate(hours):
        s.rect(x0 + i * cw, 116, cw - 6, 28, rx=8, fill="#ffffff", stroke=ORANGE)
        s.text(x0 + i * cw + (cw - 6) / 2, 135, "%d:00" % h, size=12, fill=ORANGE, anchor="middle", weight=800)
    for r, (who, b) in enumerate(busy.items()):
        y = 152 + r * 36
        s.text(24, y + 20, who, size=13, weight=800)
        for i, h in enumerate(hours):
            bad = h in b
            s.rect(x0 + i * cw, y, cw - 6, 30, rx=6, fill=("#ffe3e3" if bad else "#ebfbee"), stroke=("#ffa8a8" if bad else "#b2f2bb"))
            if bad:
                s.text(x0 + i * cw + (cw - 6) / 2, y + 19, "busy", size=10.5, fill=RED, anchor="middle", weight=800)
    s.text(24, 278, "Omar works from home on Sunday.", size=13, weight=800)
    s.text(24, 312, "Where?", size=13, weight=800)
    s.rect(84, 294, 100, 28, rx=8, fill="#ffffff", stroke=ORANGE)
    s.text(134, 313, "Room 21", size=12.5, fill=ORANGE, anchor="middle", weight=800)
    s.rect(194, 294, 130, 28, rx=8, fill="#ffffff", stroke=ORANGE)
    s.text(259, 313, "Online (Teams)", size=12.5, fill=ORANGE, anchor="middle", weight=800)
    s.save(os.path.join(W3, "sims", "meeting-planner.svg"))


def poster_team_desk():
    s = Svg(640, 360)
    s.text(24, 34, "Team Desk at Sunrise Company", size=21, weight=800)
    s.text(24, 56, "Help your colleagues to send, meet and share files.", size=12, fill=MUTED)
    s.text(24, 88, "Message 1 / 8", size=13, weight=800)
    s.text(616, 88, "0 stars", size=13, fill=ORANGE, anchor="end", weight=800)
    s.rect(24, 102, 500, 74, rx=14, fill=SOFT, stroke=PEACH)
    s.text(38, 122, "Lina (office)", size=10.5, fill=MUTED, weight=700)
    s.lines(38, 142, ["I sent an e-mail to ten people. One of them asks me a", "question, only for me. How do I answer?"], size=12.5, weight=800, gap=18)
    for i, t in enumerate(["Reply", "Reply all", "Forward"]):
        y = 194 + i * 42
        s.rect(24, y, 592, 34, rx=10, fill="#ffffff", stroke=ORANGE)
        s.text(38, y + 22, t, size=13, fill=ORANGE, weight=800)
    s.save(os.path.join(W3, "sims", "team-desk.svg"))


def message(s, x, y, w, rows, num=True):
    """A message card; rows: (text, size, weight, color, badge number or None)."""
    h = 26 + 26 * len(rows)
    s.rect(x, y, w, h, rx=12, fill="#ffffff", stroke=LINE)
    for i, (t, size, weight, color, n) in enumerate(rows):
        yy = y + 30 + i * 26
        s.text(x + 16, yy, t, size=size, fill=color, weight=weight)
        if n and num:
            s.badge(x + w + 16, yy - 4, n)
    return h


def phish_model():
    """Step 2 model: a fake bank e-mail with its four warning signs."""
    s = Svg(790, 236)
    rows = [("From: Sunrise Bank <service@sunrise-bank-help.co>", 12.5, 800, INK, 1),
            ("Subject: Your card is blocked", 12.5, 800, INK, None),
            ("Dear customer,", 12.5, 600, INK, None),
            ("Your card is blocked. Open it in 12 hours, or you lose it!", 12.5, 700, RED, 2),
            ("Sign in here: sunrise-bank-help.co/login", 12.5, 700, BLUE, 3),
            ("Type your card number and your PIN to open it.", 12.5, 700, INK, 4),
            ("Thank you, Sunrise Bank", 12.5, 600, INK, None)]
    message(s, 20, 14, 450, rows)
    notes = ["1  The address is not the bank's.", "2  It hurries you, with a threat.", "3  The link goes to a strange site.",
             "4  It asks for your PIN."]
    for i, t in enumerate(notes):
        s.text(522, 50 + i * 30, t, size=12, weight=800)
    s.save(os.path.join(W3, "images", "phish-model.svg"))


def phish_task():
    """Task 2: the mailbox e-mail with six numbered parts (three are warning signs: 1, 3, 4)."""
    s = Svg(560, 212)
    rows = [("From: Mail Team <mailteam@m4il-box-help.net>", 12.5, 800, INK, 1),
            ("Sunday, 9:12", 12, 600, MUTED, 2),
            ("You lose all your e-mails in 24 hours!", 12.5, 700, INK, 3),
            ("Type your university password on this page.", 12.5, 700, INK, 4),
            ("Thank you.", 12.5, 600, INK, 5),
            ("Mail Team", 12.5, 600, INK, 6)]
    message(s, 20, 14, 470, rows)
    s.save(os.path.join(W3, "images", "phish-task.svg"))


def poster_password_check():
    s = Svg(640, 380)
    s.text(24, 34, "Password Check: weak or strong?", size=21, weight=800)
    s.text(24, 56, "Type a made-up password, or tap an example.", size=12, fill=MUTED)
    s.rect(24, 70, 592, 32, rx=10, fill=SOFT, stroke=PEACH, dash="6 4")
    s.text(36, 91, "Never type your real password here.", size=12.5, weight=800)
    s.rect(24, 116, 420, 36, rx=10, fill="#ffffff", stroke=LINE)
    s.text(36, 140, "Blue-Camel-Rain-47", size=15, weight=700)
    s.rect(24, 164, 420, 14, rx=7, fill="#e9ecef", stroke=None)
    s.rect(24, 164, 420, 14, rx=7, fill=GREEN, stroke=None)
    s.text(24, 200, "Strength: Strong", size=14, fill=GREEN, weight=800)
    for i, t in enumerate(["At least 12 characters (now 18)", "Three kinds: letters, capitals, numbers, symbols",
                           "No common word, name or year"]):
        s.tick(32, 226 + i * 26, c=GREEN, k=0.8)
        s.text(46, 230 + i * 26, t, size=12.5, fill=GREEN, weight=700)
    s.text(24, 318, "Examples:", size=12.5, weight=800)
    x = 24
    for e in ["sami2005", "Password123", "qwerty", "green lamp river 82"]:
        w = 16 + 8 * len(e)
        s.rect(x, 330, w, 28, rx=8, fill="#ffffff", stroke=ORANGE)
        s.text(x + w / 2, 349, e, size=12, fill=ORANGE, anchor="middle", weight=800)
        x += w + 8
    s.save(os.path.join(W3, "sims", "password-check.svg"))


def poster_phish_finder():
    s = Svg(640, 300)
    s.text(24, 34, "Phish Finder: safe or phishing?", size=21, weight=800)
    s.text(24, 56, "Read each message. Is it safe, or a fake message that wants your password?", size=12, fill=MUTED)
    s.text(24, 88, "Message 1 / 6", size=13, weight=800)
    s.text(616, 88, "0 right", size=13, fill=ORANGE, anchor="end", weight=800)
    s.rect(24, 100, 520, 96, rx=14, fill="#ffffff", stroke=LINE)
    s.text(38, 122, "SMS · From: +962 7 9000 1111", size=11, fill=MUTED, weight=700)
    s.text(38, 146, "You won a new phone! Pay 2 JD for the delivery", size=13, weight=700)
    s.text(38, 166, "today:", size=13, weight=700)
    s.text(84, 166, "win-phone-jo.top/pay", size=13, fill=BLUE, weight=800)
    for i, t in enumerate(["Safe", "Phishing"]):
        x = 24 + i * 96
        s.rect(x, 214, 86, 34, rx=10, fill="#ffffff", stroke=ORANGE)
        s.text(x + 43, 236, t, size=13, fill=ORANGE, anchor="middle", weight=800)
    s.save(os.path.join(W3, "sims", "phish-finder.svg"))


if __name__ == "__main__":
    email_parts()
    meeting_invite()
    co_editing()
    poster_mail_lab()
    poster_meeting_planner()
    poster_team_desk()
    phish_model()
    phish_task()
    poster_password_check()
    poster_phish_finder()
