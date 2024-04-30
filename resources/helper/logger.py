# creating a function to create a .log file and write some infos in it

def log(inf: dict) -> None:
    with open(".log", "a", encoding="utf-8") as log:
        for key in inf:
            log.write(f"""{key}: {inf[key]}\n""")
        log.write("\n\n")