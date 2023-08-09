import pygame as pg

running = True
fps = 60
scSize = [1000, 600]
bgColor = (20, 20, 30)

mainFontStyle = 'arial'
mainFontSize = 30

pg.init()
pg.font.init()
pg.display.init()

mainFont = pg.font.SysFont(mainFontStyle, mainFontSize)
clock = pg.time.Clock()
sc = pg.display.set_mode(scSize, pg.RESIZABLE)