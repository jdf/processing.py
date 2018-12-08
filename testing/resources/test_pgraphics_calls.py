# make sure that ellipse, arc, line, and rect all work as functions

size(100, 100)
pg = createGraphics(40, 40)

pg.beginDraw()

pg.ellipse(20, 20, 10, 10)
pg.line(30, 30, 40, 40)
pg.rect(0, 0, 10, 10)
pg.arc(30, 35, 30, 30, 0, HALF_PI)
pg.endDraw()
image(pg, 9, 30)

print 'OK'
exit()
