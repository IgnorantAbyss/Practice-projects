def stripblank(textlist):
    t = 0
    for i in range (len(textlist)):
        if len(textlist[i]) == 0:
            t += 1
    for i in range(t):
        textlist.remove("")
    return textlist
