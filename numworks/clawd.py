# Clawd Catch - mini jeu NumWorks
# Fleches gauche/droite : bouger
# Attrape les {} (+1) et les etoiles (+5)
# Evite les bugs rouges ! 3 vies.
# OK / EXE : jouer   Retour (Back) : quitter

from kandinsky import fill_rect, draw_string
from ion import keydown, KEY_LEFT, KEY_RIGHT, KEY_OK, KEY_EXE, KEY_BACK
from time import sleep, monotonic
from random import randint

W, H = 320, 222
BG = (24, 24, 32)
OR = (217, 119, 87)
RD = (230, 60, 60)
BK = (20, 20, 20)
GR = (90, 220, 120)
YL = (255, 210, 60)
WH = (240, 240, 240)

# Clawd, la mascotte : O = orange, K = yeux, . = fond
BODY = (".OOOOOOOOO.",
        ".OKOOOOOKO.",
        "OOOOOOOOOOO",
        "OOOOOOOOOOO",
        ".OOOOOOOOO.")
LEGS = (".O.O...O.O.", "O.O.....O.O")
S = 3
PW, PH = 33, 18
PY = H - PH - 2
TOP = 22


def sprite(x, y, s, leg, col):
  rows = BODY + (LEGS[leg],)
  for j in range(6):
    row = rows[j]
    i = 0
    while i < 11:
      c = row[i]
      k = i
      while k < 11 and row[k] == c:
        k += 1
      fill_rect(x + i * s, y + j * s, (k - i) * s, s,
                col if c == "O" else (BK if c == "K" else BG))
      i = k


def draw_item(t, x, y):
  if t == 0:
    draw_string("{}", x, y, GR, BG)
  elif t == 1:
    fill_rect(x + 4, y + 4, 12, 10, RD)
    fill_rect(x, y + 6, 20, 2, RD)
    fill_rect(x, y + 11, 20, 2, RD)
    fill_rect(x + 6, y + 6, 2, 2, WH)
    fill_rect(x + 12, y + 6, 2, 2, WH)
  else:
    draw_string("*", x + 5, y, YL, BG)


def hud(sc, lv, best):
  fill_rect(0, 0, W, TOP - 1, BG)
  draw_string("Score " + str(sc), 4, 1, WH, BG)
  draw_string("Best " + str(best), 130, 1, OR, BG)
  draw_string("<3" * lv, 316 - 20 * lv, 1, RD, BG)
  fill_rect(0, TOP - 1, W, 1, OR)


def wait_start():
  while keydown(KEY_OK) or keydown(KEY_EXE):
    sleep(0.02)
  while True:
    if keydown(KEY_OK) or keydown(KEY_EXE):
      return True
    if keydown(KEY_BACK):
      return False
    sleep(0.02)


def title():
  fill_rect(0, 0, W, H, BG)
  draw_string("CLAWD CATCH", 105, 18, OR, BG)
  sprite(127, 60, 6, 0, OR)
  draw_string("Attrape les {} et les *", 45, 120, GR, BG)
  draw_string("Evite les bugs !", 80, 142, RD, BG)
  draw_string("OK pour jouer", 95, 185, WH, BG)


def game(best):
  fill_rect(0, 0, W, H, BG)
  px = (W - PW) // 2
  sc, lv, t, leg, hurt = 0, 3, 0, 0, 0
  items = []
  hud(sc, lv, best)
  while lv > 0:
    t0 = monotonic()
    t += 1
    sp = 2 + sc // 15
    # deplacement
    nx = px
    if keydown(KEY_LEFT):
      nx = max(0, px - 6)
    if keydown(KEY_RIGHT):
      nx = min(W - PW, px + 6)
    if nx != px:
      if nx > px:
        fill_rect(px, PY, nx - px, PH, BG)
      else:
        fill_rect(nx + PW, PY, px - nx, PH, BG)
      px = nx
      if t % 3 == 0:
        leg ^= 1
    # apparition
    if t % max(8, 28 - sc // 4) == 0:
      r = randint(0, 19)
      ty = 2 if r == 0 else (1 if r < 7 + min(6, sc // 20) else 0)
      items.append([ty, randint(0, W - 20), TOP])
    # chute
    keep = []
    for it in items:
      ty, x, y = it
      fill_rect(x, y, 20, 18, BG)
      y += sp
      if y + 16 > PY and y < PY + PH and x + 18 > px and x + 2 < px + PW:
        if ty == 1:
          lv -= 1
          hurt = 10
        else:
          sc += 5 if ty == 2 else 1
        hud(sc, lv, max(sc, best))
      elif y < H:
        it[2] = y
        draw_item(ty, x, y)
        keep.append(it)
    items = keep
    if hurt:
      hurt -= 1
    sprite(px, PY, S, leg, RD if hurt and t % 2 else OR)
    if keydown(KEY_BACK):
      break
    dt = 0.03 - (monotonic() - t0)
    if dt > 0:
      sleep(dt)
  return sc


def main():
  best = 0
  title()
  if not wait_start():
    return
  while True:
    sc = game(best)
    best = max(best, sc)
    fill_rect(60, 70, 200, 90, BK)
    fill_rect(60, 70, 200, 2, OR)
    fill_rect(60, 158, 200, 2, OR)
    draw_string("GAME OVER", 115, 80, RD, BK)
    draw_string("Score : " + str(sc), 100, 105, WH, BK)
    draw_string("OK : rejouer", 100, 130, OR, BK)
    sleep(0.5)
    if not wait_start():
      return


main()
