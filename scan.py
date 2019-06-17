import os


def get_token(s):
    r = ''
    for i, e in enumerate(s):
        if e in ') ':
            r = s[:i]
            break
    if len(s) >= 1 and r == '':
        r = s
    return r


def format_token(s):
    num = '0123456789'
    if s[0] in num:
        return int(s)
    elif s == 'True':
        return True
    elif s == 'False':
        return False
    else:
        return s


def init_list(s):
    l = []
    count = 0
    for i, e in enumerate(s):
        if count > 0:
            count -= 1
            continue
        elif e in '()':
            l.append(e)
        elif e == ' ':
            pass
        else:
            token = get_token(s[i:])
            count = len(token) - 1
            token = format_token(token)
            l.append(token)
    return l


def get_list(l):
    r = []
    count = 0
    self_count = 0
    for i, e in enumerate(l):
        if count > 0:
            count -= 1
            continue
        self_count += 1
        if e == ')':
            break
        elif e == '(':
            child_list, child_count = get_list(l[i+1:])
            count = child_count
            self_count += child_count
            r.append(child_list)
        else:
            r.append(e)
    return r, self_count


# 检测define是否发生错误
def check_define(l):
    flag = True
    # print(l)
    for i, e in enumerate(l):
        if e == '(':
            continue
        if e == 'define':
            if flag:
                flag = False
            else:
                print("define syntax error(语法错误)")
                os._exit(0)


def parse(s):
    l = init_list(s)
    print(l)
    check_define(l)
    r, c = get_list(l)
    print(r)
    return r[0]
