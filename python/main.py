import reengine as re 

r = re.compile("S(a|g|r)+on")

print(r.match_line("Sagron"))