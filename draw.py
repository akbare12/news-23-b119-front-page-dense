"""news-23 b119 front-page-dense: draw THE WORLD TODAY, Monday 23 Nov 2026.

Layout (1024x1024), front-page-dense:
masthead -> kicker -> number strip (2 rows x 5) -> region bar -> UTC strip
-> 3 hero scenes -> MORE OF THE DAY (10 cards) -> WHERE IT HAPPENED
(map + pins + ALSO 18) -> DATE CHECK red box -> footer.
Run: python3 draw.py  (writes entry.png next to this file)
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (250, 247, 238)          # warm paper
INK = (20, 20, 20)
BLACK = (0, 0, 0)
RED = (185, 28, 28)
GOLD = (212, 175, 55)
NAVY = (13, 27, 62)
GREY = (90, 90, 90)
CREAM = (245, 240, 225)

F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    """Wrap text to fit max_w pixels; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def chip(d, x, y, text, fill, fnt, h=11, fg=(255, 255, 255)):
    """Small filled label; returns width."""
    w = int(d.textlength(text, font=fnt)) + 8
    d.rounded_rectangle([x, y, x + w, y + h], radius=2, fill=fill)
    d.text((x + 4, y + 1), text, font=fnt, fill=fg)
    return w


def draw():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.rectangle([0, 0, W, 58], fill=BLACK)
    d.text((16, 7), "THE WORLD TODAY", font=font(F_SERIF, 44), fill=(255, 255, 255))
    date_f = font(F_SANSB, 15)
    dt = "MONDAY 23 NOVEMBER 2026"
    d.text((W - 16 - d.textlength(dt, font=date_f), 20), dt, font=date_f, fill=GOLD)

    # ---------- kicker ----------
    d.rectangle([0, 58, W, 80], fill=RED)
    kf = font(F_SANSB, 13)
    kick = "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B"
    d.text(((W - d.textlength(kick, font=kf)) / 2, 63), kick, font=kf, fill=(255, 255, 255))

    # ---------- number strip: 2 rows x 5 cols, value over label ----------
    strip = [
        [("\u22123.3%", "KOSPI"), ("5.3", "US\u2013CHINA POWER GAP"),
         ("11,762", "EBOLA CASES, DRC"), ("10T won", "SEOUL STABILISATION FUND"),
         ("2%", "BILLIONAIRE TAX IN PARIS")],
        [("$450M", "SKUBAL DEAL"), ("165", "RUSSIAN MISSILES/WEEK"),
         ("12,000", "CLEARED IN MANCHESTER"), ("264 kg", "EXPLOSIVES SEIZED"),
         ("$107.3B", "ANTHROPIC IPO")],
    ]
    vf, lf = font(F_SANSB, 18), font(F_SANS, 8)
    cw = W / 5
    for r, row in enumerate(strip):
        y0 = 80 + r * 33
        for c, (val, lab) in enumerate(row):
            x0 = c * cw
            d.text((x0 + 10, y0 + 4), val, font=vf, fill=INK)
            d.text((x0 + 10, y0 + 24), lab, font=lf, fill=GREY)
        d.line([0, y0 + 32, W, y0 + 32], fill=(210, 205, 190), width=1)

    # ---------- region bar ----------
    regions = [("ASIA-PACIFIC 7", (30, 58, 138)), ("AMERICAS 8", (185, 28, 28)),
               ("MIDDLE EAST 6", (15, 120, 110)), ("EUROPE 5", (110, 70, 160)),
               ("AFRICA 3", (40, 130, 70)), ("WORLD 2", (70, 70, 70))]
    rf = font(F_SANSB, 11)
    x = 0
    for name, col in regions:
        wseg = W / len(regions)
        d.rectangle([x, 146, x + wseg, 168], fill=col)
        tw = d.textlength(name, font=rf)
        d.text((x + (wseg - tw) / 2, 152), name, font=rf, fill=(255, 255, 255))
        x += wseg

    # ---------- UTC strip ----------
    uf = font(F_SANS, 10)
    d.text((10, 171), "THE DAY IN UTC  \u00b7  ~00:00 Kospi dives  \u00b7  ~05:30 Guterres opens  "
                      "\u00b7  ~09:00 Power Index  \u00b7  ~12:00 Paris 2% tax  \u00b7  ~15:00 Kyiv missiles",
           font=uf, fill=GREY)
    d.text((W - 10 - d.textlength("~ APPROX", font=uf), 171), "~ APPROX", font=uf, fill=GREY)

    # ---------- hero scenes ----------
    HX = [8, 346, 684]
    HW = 330
    SY, SH = 184, 100  # scene y, height

    # --- scene 1: Kospi skyline + falling chart ---
    x0 = HX[0]
    d.rectangle([x0, SY, x0 + HW, SY + SH], fill=NAVY)
    # buildings with lit windows
    import random
    rnd = random.Random(23)
    bx = x0 + 6
    while bx < x0 + HW - 30:
        bw, bh = rnd.randint(22, 38), rnd.randint(30, 62)
        d.rectangle([bx, SY + SH - bh, bx + bw, SY + SH], fill=(24, 42, 84))
        for wy in range(SY + SH - bh + 5, SY + SH - 4, 9):
            for wx in range(bx + 4, bx + bw - 3, 8):
                if rnd.random() < 0.55:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 90))
        bx += bw + 4
    # orange chart line, kept below the -3.3% text (starts y+55)
    pts = [(x0 + 12, SY + 58), (x0 + 60, SY + 66), (x0 + 110, SY + 62),
           (x0 + 160, SY + 72), (x0 + 210, SY + 70), (x0 + 260, SY + 82),
           (x0 + 315, SY + 92)]
    d.line(pts, fill=(255, 140, 40), width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 255, 255))
    d.text((x0 + 10, SY + 6), "\u22123.3%", font=font(F_SANSB, 34), fill=(255, 255, 255))
    d.rectangle([x0, SY + SH - 16, x0 + HW, SY + SH], fill=BLACK)
    d.text((x0 + 8, SY + SH - 14), "KOSPI 4,708.54  \u00b7  \u2212161 PTS",
           font=font(F_SANSB, 10), fill=(255, 255, 255))

    # --- scene 2: Guterres, green + gold 150 ---
    x0 = HX[1]
    d.rectangle([x0, SY, x0 + HW, SY + SH], fill=(29, 107, 52))
    d.text((x0 + 12, SY + 4), "150", font=font(F_SANSB, 36), fill=GOLD)
    gf = font(F_SANSB, 15)
    for i, line in enumerate(["DELEGATES", "BACK A RISK", "FRAMEWORK"]):
        d.text((x0 + 12, SY + 44 + i * 17), line, font=gf, fill=GOLD)
    # globe, right side
    cx, cy, r = x0 + 268, SY + 50, 38
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(190, 230, 190))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(29, 107, 52), width=2)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=(29, 107, 52), width=1)
    d.line([cx - r, cy, cx + r, cy], fill=(29, 107, 52), width=1)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360, fill=(29, 107, 52), width=1)

    # --- scene 3: Power Index bars ---
    x0 = HX[2]
    d.rectangle([x0, SY, x0 + HW, SY + SH], fill=CREAM)
    tf = font(F_SANSB, 11)
    d.text((x0 + 10, SY + 6), "NARROWEST SINCE 2018", font=tf, fill=INK)
    gap = "GAP 5.3"
    d.text((x0 + HW - 10 - d.textlength(gap, font=tf), SY + 6), gap, font=tf, fill=RED)
    bars = [("78.9", "US", (30, 58, 138), 50), ("73.6", "CHINA", (185, 28, 28), 46),
            ("40.5", "INDIA", (176, 141, 30), 27)]
    base = SY + SH - 12
    bw, gapx = 62, 34
    bx = x0 + 28
    bf = font(F_SANSB, 13)
    lf2 = font(F_SANSB, 10)
    for val, lab, col, bh in bars:
        d.text((bx + (bw - d.textlength(val, font=bf)) / 2, base - bh - 16), val,
               font=bf, fill=INK)
        d.rectangle([bx, base - bh, bx + bw, base], fill=col)
        d.text((bx + (bw - d.textlength(lab, font=lf2)) / 2, base + 1), lab,
               font=lf2, fill=INK)
        bx += bw + gapx

    # ---------- hero headline blocks ----------
    heroes = [
        ("AI ROUT HITS ASIA",
         "Kospi closes \u22123.3% to 4,708.54, sheds 161 pts; intraday \u22125.8%. Samsung \u22123.1%, SK Hynix \u22122.5%.",
         "KOREA EXCHANGE"),
        ("GUTERRES: REGULATE AI BEFORE IT\u2019S TOO LATE",
         "UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework.",
         "UNITED NATIONS"),
        ("US LEAD OVER CHINA AT RECORD LOW",
         "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
         "LOWY INSTITUTE"),
    ]
    hf = font(F_SANSB, 16)
    bf2 = font(F_SANS, 11)
    sf = font(F_SANS, 9)
    cf = font(F_SANSB, 8)
    for i, (head, body, src) in enumerate(heroes):
        x0 = HX[i]
        hl = wrap(d, head, hf, HW)
        y = 288
        for line in hl[:2]:
            d.text((x0, y), line, font=hf, fill=INK)
            y += 19
        bl = wrap(d, body, bf2, HW)
        y = 328
        for line in bl[:2]:
            d.text((x0, y), line, font=bf2, fill=INK)
            y += 13
        d.text((x0, 351), src, font=sf, fill=GREY)
        chip(d, x0 + HW - 66, 350, "REPORTED", NAVY, cf)

    # ---------- MORE OF THE DAY strip ----------
    d.rectangle([0, 366, W, 384], fill=BLACK)
    d.text((10, 370), "MORE OF THE DAY  \u2014  10 STORIES", font=font(F_SANSB, 12),
           fill=(255, 255, 255))

    # ---------- 10 cards: 5 cols x 2 rows ----------
    cards = [
        ("AMERICAS", (185, 28, 28), "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "WSJ", "REPORTED"),
        ("AMERICAS", (185, 28, 28), "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED"),
        ("WHITE HOUSE", (110, 70, 160), "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED"),
        ("MARKETS", (15, 120, 110), "US FUTURES JUMP 3%", "Holiday rally lifts 3%.", "Bloomberg", "REPORTED"),
        ("SPORT", (176, 141, 30), "SKUBAL\u2019S $450M METS DEAL", "Nine-year, largest ever.", "AP", "REPORTED"),
        ("SPORT", (176, 141, 30), "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.", "ESPN", "REPORTED"),
        ("LEGAL", (70, 70, 70), "STATES SUE SPACEX", "Ten states sue over AI.", "AP", "REPORTED"),
        ("TECH", (30, 58, 138), "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.", "WSJ", "REPORTED"),
        ("EUROPE", (110, 70, 160), "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: 3 Kh-101s crossed.", "AP", "CLAIM"),
        ("SPACE", (15, 120, 110), "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM"),
    ]
    tagf, chf, cbf = font(F_SANSB, 8), font(F_SANSB, 12), font(F_SANS, 10)
    cw2 = (W - 16 - 4 * 6) / 5
    for idx, (cat, col, head, body, src, kind) in enumerate(cards):
        r, c = divmod(idx, 5)
        x0 = 8 + c * (cw2 + 6)
        y0 = 384 + r * 64
        d.rectangle([x0, y0, x0 + cw2, y0 + 64], outline=(210, 205, 190), width=1)
        d.text((x0 + 6, y0 + 4), cat, font=tagf, fill=col)
        num = str(idx + 1)
        d.text((x0 + cw2 - 6 - d.textlength(num, font=tagf), y0 + 4), num,
               font=tagf, fill=RED)
        hl = wrap(d, head, chf, cw2 - 12)
        y = y0 + 18
        for line in hl[:2]:
            d.text((x0 + 6, y), line, font=chf, fill=INK)
            y += 13
        d.text((x0 + 6, y0 + 45), body, font=cbf, fill=INK)
        d.text((x0 + 6, y0 + 54), src, font=sf, fill=GREY)
        cfill = NAVY if kind == "REPORTED" else RED
        chip(d, x0 + cw2 - 6 - 62, y0 + 53, kind, cfill, cf, h=10)

    # ---------- WHERE IT HAPPENED strip ----------
    d.rectangle([0, 512, W, 530], fill=BLACK)
    d.text((10, 516), "WHERE IT HAPPENED", font=font(F_SANSB, 12), fill=(255, 255, 255))

    # ---------- map: simplified world blobs + 13 pins ----------
    MAPX, MAPY = 8, 534
    GREEN = (190, 220, 170)
    # Americas blob (rough)
    d.polygon([(MAPX + 16, MAPY + 6), (MAPX + 96, MAPY + 6), (MAPX + 104, MAPY + 60),
               (MAPX + 84, MAPY + 110), (MAPX + 66, MAPY + 150), (MAPX + 58, MAPY + 210),
               (MAPX + 66, MAPY + 246), (MAPX + 40, MAPY + 250), (MAPX + 30, MAPY + 200),
               (MAPX + 24, MAPY + 140), (MAPX + 8, MAPY + 90), (MAPX + 6, MAPY + 30)],
              fill=GREEN)
    # Europe blob
    d.polygon([(MAPX + 150, MAPY + 8), (MAPX + 216, MAPY + 8), (MAPX + 222, MAPY + 44),
               (MAPX + 200, MAPY + 70), (MAPX + 164, MAPY + 66), (MAPX + 146, MAPY + 36)],
              fill=GREEN)
    # Africa blob
    d.polygon([(MAPX + 150, MAPY + 78), (MAPX + 216, MAPY + 78), (MAPX + 208, MAPY + 130),
               (MAPX + 186, MAPY + 176), (MAPX + 168, MAPY + 150), (MAPX + 152, MAPY + 110)],
              fill=GREEN)
    # Asia blob
    d.polygon([(MAPX + 222, MAPY + 8), (MAPX + 318, MAPY + 8), (MAPX + 322, MAPY + 60),
               (MAPX + 300, MAPY + 110), (MAPX + 262, MAPY + 130), (MAPX + 236, MAPY + 96),
               (MAPX + 224, MAPY + 50)], fill=GREEN)
    pins = [(300, 580, "1"), (98, 655, "2"), (288, 562, "3"), (58, 602, "4"),
            (78, 584, "5"), (195, 578, "6"), (172, 592, "7"), (165, 572, "8"),
            (215, 560, "9"), (150, 550, "10"), (228, 612, "11"), (218, 630, "12"),
            (185, 682, "13")]
    pf = font(F_SANSB, 9)
    for px, py, n in pins:
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
        tw = d.textlength(n, font=pf)
        d.text((px - tw / 2, py - 6), n, font=pf, fill=(255, 255, 255))
    # legend, 4 short lines under the blobs
    lgf = font(F_SANS, 9)
    legend = ["Pins 1\u201313: 1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing",
              "4 Washington \u00b7 5 New York \u00b7 6 Kyiv \u00b7 7 Paris",
              "8 London \u00b7 9 Warsaw \u00b7 10 Manchester \u00b7 11 Beirut",
              "12 Gaza \u00b7 13 Khartoum"]
    for i, line in enumerate(legend):
        d.text((MAPX + 2, 792 + i * 11), line, font=lgf, fill=INK)

    # ---------- ALSO ON MONDAY ----------
    d.text((340, 540), "ALSO ON MONDAY", font=font(F_SANSB, 13), fill=INK)
    also = [
        "14. Paris: 100+ back 2% billionaire tax",
        "15. Manchester: 12,000 cleared",
        "16. Zelenskyy: 165 missiles in a week",
        "17. COP31: the day after Antalya pact rejected",
        "18. Israel unity talks resume",
        "19. Gaza: two killed in Israeli strike",
        "20. West Bank settler attacks",
        "21. Iran war: no deal in sight",
        "22. Lebanon seizes 264 kg explosives",
        "23. Bahrain: strike hits plant, 2 hurt",
        "24. Benghazi: UN demands probe",
        "25. Sudan: defences down drones",
        "26. DRC: fighting traps Ebola teams",
        "27. Bangladesh: Hasina jailed if she returns",
        "28. Seoul minister quits in exam row",
        "29. SK Telecom \u22127.3% as hype cools",
        "30. China eases margin rules",
        "31. Seoul readies 10T-won fund",
    ]
    af = font(F_SANS, 11)
    for i, item in enumerate(also):
        col = 0 if i < 9 else 1
        row = i % 9
        x = 340 if col == 0 else 680
        d.text((x, 564 + row * 30), item, font=af, fill=INK)
        if "[CLAIM]" in item:
            pass
    # red [CLAIM] tags for items 24 and 25 (right of the text).
    # ALSO rows: items 14-22 in col 0 rows 0-8, items 23-31 in col 1 rows 0-8,
    # so item 24 is col 1 row 1 (y 594) and item 25 is col 1 row 2 (y 624).
    d.text((680 + d.textlength("24. Benghazi: UN demands probe", font=af) + 6, 564 + 1 * 30),
           "[CLAIM]", font=font(F_SANSB, 10), fill=RED)
    d.text((680 + d.textlength("25. Sudan: defences down drones", font=af) + 6, 564 + 2 * 30),
           "[CLAIM]", font=font(F_SANSB, 10), fill=RED)

    # ---------- DATE CHECK red box ----------
    d.rectangle([8, 838, W - 8, 920], outline=RED, width=2)
    d.text((16, 846), "DATE CHECK  \u2014  READ 23 NOV 2026, 23:59 UTC  \u00b7  STORIES DATED 23 NOV ONLY",
           font=font(F_SANSB, 12), fill=RED)
    df = font(F_SANS, 10)
    left = ("LEFT OUT \u2014 NOT 23 NOV: Dems reach 258 (22 Nov) \u00b7 Sparta II fire (22 Nov) "
            "\u00b7 El Chapo Isidro captured (22 Nov) \u00b7 EU\u2013Indonesia pact (21 Nov) "
            "\u00b7 Nigeria boat (21 Nov) \u00b7 ICJ Myanmar ruling (19 Nov)")
    ll = wrap(d, left, df, W - 32)
    y = 866
    for line in ll[:2]:
        d.text((16, y), line, font=df, fill=INK)
        y += 13
    d.text((16, 898), "NOT YET \u2014 Dymer search continues (14 missing) \u00b7 4 House races uncalled "
                      "\u00b7 COP32 venue not set \u00b7 WHO evacuating trapped Ebola staff",
           font=df, fill=INK)

    # ---------- footer ----------
    ff = font(F_SANS, 10)
    d.text((16, 928), "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).",
           font=ff, fill=GREY)
    d.text((16, 944), "CHIPS: REPORTED = confirmed by wires \u00b7 CLAIM = one side\u2019s claim, not independently confirmed \u00b7 ONGOING = still developing.",
           font=ff, fill=GREY)
    d.text((16, 960), "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
           font=ff, fill=GREY)
    bf3 = font(F_SANSB, 12)
    foot = "THE WORLD TODAY  \u00b7  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions"
    d.text(((W - d.textlength(foot, font=bf3)) / 2, 990), foot, font=bf3, fill=(150, 110, 20))

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    draw()
