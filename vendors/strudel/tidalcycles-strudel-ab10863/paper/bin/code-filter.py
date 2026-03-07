#!/usr/bin/env python3

from pandocfilters import RawBlock, toJSONFilter


def toMiniREPL(key, value, format, meta):
    # print(value, file=sys.stderr)
    if key == "CodeBlock":
        return RawBlock("markdown", "<MiniRepl tune={`" + value[1] + "`} />")

if __name__ == "__main__":
    toJSONFilter(toMiniREPL)
