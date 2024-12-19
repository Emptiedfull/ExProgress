
from conversion import convert
from locate import closest

def out(p):
    con = convert(p)
    return closest(con)

print(out(0.6))
