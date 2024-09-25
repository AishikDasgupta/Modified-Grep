import sys
# import pyparsing 
# import lark 
class Pattern:
    DIGIT = "\\d"
    ALNUM = "\\w"

def match_pattern(input_line, pattern):
    if len(input_line) == 0 and len(pattern) == 0:
        return True
    if not pattern:
        return True
    if not input_line:
        return False
    # "^" operator
    if pattern[0] == "^":
        pattern = pattern[1:]
        while len(pattern) > 0 and len(input_line) > 0:
            if pattern[0] == input_line[0]:
                pattern = pattern[1:]
                input_line = input_line[1:]
            else:
                return False
        return match_pattern(input_line, pattern)
    # "$" operator
    if pattern[-1] == "$":
        pattern = pattern[:-1]
        while len(pattern) > 0 and len(input_line) > 0:
            if pattern[-1] == input_line[-1]:
                pattern = pattern[:-1]
                input_line = input_line[:-1]
            else:
                return False
        return match_pattern(input_line, pattern)
    # "+" operator
    if pattern[0] == input_line[0]:
        if len(pattern) > 1:
            if pattern[1] == "+":
                return match_pattern(input_line[1:], pattern[2:]) or match_pattern(
                    input_line[1:], pattern
                )
            elif pattern[1] == "?":
                return match_pattern(input_line[1:], pattern[2:]) or match_pattern(
                    input_line, pattern[1:]
                )
        return match_pattern(input_line[1:], pattern[1:])
    # "?" operator
    elif pattern[0] != input_line[0] and len(pattern) > 1 and pattern[1] == "?":
        if pattern[1] == "?":
            return match_pattern(input_line, pattern[2:])
        return False
    # "." operator
    elif pattern[0] == ".":
        return match_pattern(input_line[1:], pattern[1:])
    # "|" operator
    elif pattern.startswith("(") and ")" in pattern:
        first, second = pattern[1 : pattern.index(")")].split("|")
        pattern_truncated = pattern[pattern.index(")") + 1 :]
        return match_pattern(input_line, first + pattern_truncated) or match_pattern(input_line, second + pattern_truncated)
    # /d operator
    elif pattern[:2] == Pattern.DIGIT:
        for i in range(len(input_line)):
            if input_line[i].isdigit():
                return match_pattern(input_line[i:], pattern[2:])
        else:
            return False
    # /w operator    
    elif pattern[:2] == Pattern.ALNUM:
        if input_line[0].isalnum():
            return match_pattern(input_line[1:], pattern[2:])
        else:
            return False
    # "[^abc]" operator    
    elif pattern[0] == "[" and pattern[-1] == "]":
        if pattern[1] == "^":
            chrs = list(pattern[2:-1])
            for c in chrs:
                if c in input_line:
                    return False
            return True
        chrs = list(pattern[1:-1])
        for c in chrs:
            if c in input_line:
                return True
        return False
    else:
        return match_pattern(input_line[1:], pattern)
    

def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()
    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)
    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)
        
if __name__ == "__main__":
    main()