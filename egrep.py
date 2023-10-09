import reengine as re 
import sys

def main(regex_string):
    # No need to compile for an empty regex.
    if regex_string == "":
        return
    # regex_string = f".*{regex_string}.*" # match the entire line # Bad fix
    try: 
        matcher = re.compile(regex_string)
    except Exception as e:
        print(f"An error occured: {e}")

    try:
        for line in sys.stdin:
            line = line.rstrip()
            if matcher.match_line(line):
                print(line)
    except KeyboardInterrupt:
        pass # exit peacefully
    except Exception as e:
        print(f"Other exception occured! {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 main.py [regex]")
    else:
        regex_string = sys.argv[1]
        main(regex_string)
    


