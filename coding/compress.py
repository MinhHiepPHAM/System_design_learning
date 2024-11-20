def compress(chars: List[str]) -> int:
    cnt = ptr = length = 0
    cur_char = chars[0]
    max_len = len(chars) - 1

    for i, ch in enumerate(chars):
        if cur_char == ch:
            cnt += 1
        else:
            chars[ptr] = cur_char
            ptr += 1
            length += 1
            if cnt > 1:
                for c in str(cnt):
                    chars[ptr] = c
                    ptr += 1
                    length += 1
            cur_char = ch
            cnt = 1
        if i == max_len:
            chars[ptr] = ch
            length += 1
            if cnt > 1:
                for c in str(cnt):
                    ptr += 1
                    chars[ptr] = c
                    length += 1
    return length

                

