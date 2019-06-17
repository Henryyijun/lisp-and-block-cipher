class Node:
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value

    def __str__(self):
        return self.value + '\n' + self.kind


def get(s):
    a = type(s)
    if a == type or a == str:
        if s == int:
            kind = 'Int'
        elif s == bool:
            kind = 'Bool'
        else:
            kind = s
        value = 'define'
    else:
        value = s
        if a == int:
            kind = 'Int'
        elif a == bool:
            kind = 'Bool'
        else:
            kind = 'error'
    return Node(kind, value)


class Lisp:
    def __init__(self, variable=None, function=None, global_variable=None, pre_node=None):
        if variable is None:
            variable = {}
        if function is None:
            function = {}
        if global_variable is None:
            global_variable = {}
        if pre_node is None:
            pre_node = []

        self.var = variable
        self.func = function
        self.global_v = global_variable
        self.pre = pre_node

    def control(self, lisp):
        op = {'+': self.add,
              '-': self.minus,
              '*': self.multi,
              '/': self.divide,
              'define': self.define,
              'eq?': self.eq,
              'cond': self.cond
             }

        if type(lisp) is list:
            if type(lisp[0]) is list and lisp[0][0] == 'lambda':
                result = self.handle_lambda(lisp[0], lisp[1:])
            elif lisp[0] in self.func.keys():
                result = self.call_func(lisp)
            else:
                operation = lisp[0]
                result = op[operation](lisp)
        elif type(lisp) == str:
            result = self.get_v(lisp)
        else:
            result = lisp
        return result

    def add(self, l):
        result = self.control(l[1])
        for i, e in enumerate(l):
            if i < 2:
                continue
            result += self.control(e)
        return result

    def minus(self, l):
        result = self.control(l[1])
        for i, e in enumerate(l):
            if i < 2:
                continue
            result -= self.control(e)
        return result

    def multi(self, l):
        result = self.control(l[1])
        for i, e in enumerate(l):
            if i < 2:
                continue
            result *= self.control(e)
        return result

    def divide(self, l):
        result = self.control(l[1])
        for i, e in enumerate(l):
            if i < 2:
                continue
            if e != 0:
                result /= self.control(e)
        return int(result)

    def define(self, l):
        '''
        :param l:[define, a, 5] , [define, f, [lambda, [x, y],[x + y]]]
        :return:
        '''
        if type(l[2]) == list and l[2][0] == 'lambda':
            return self.define_function(l)
        else:
            return self.define_variable(l)

    def define_function(self, l):
        key = l[1]
        value = [l[2][1], l[2][2]]
        d = {key: value}
        self.func.update(d)
        return 'FUN'

    def define_variable(self, l):
        '''
        :param l: [define a 5]
        :return:
        '''
        key = l[1]
        value = self.control(l[2])
        self.var.update({key: value})
        self.global_v.update({key: value})
        return type(value)

    def eq(self, l):
        return self.control(l[1]) == self.control(l[2])

    def cond(self, l):
        for i, e in enumerate(l):
            if i < 1:
                continue
            if self.control(e[0]):
                return self.control(e[1])

    def get_v(self, name):
        if name in self.pre:
            return self.var[name]
        else:
            return self.global_v[name]

    def f2a(self, f, a):
        '''
        将形式参数转为实际参数
        :param f: 形式参数
        :param a: 实际参数
        :return:
        '''
        result = {}
        for i, e in enumerate(f):
            result[e] = self.control(a[i])
        return result

    def set_pre(self, l):
        if self.pre:
            self.pre.extend(l)
        else:
            self.pre = l.copy()

    def handle_lambda(self, l1, parameter):
        '''
        :param l1: lambda 表达式
        :param parameter:  实际参数
        :return:
        '''
        param = l1[1]  #形式参数
        func = l1[2]
        r = self.f2a(param, parameter)
        d = self.var.copy()
        d.update(r)
        lisp = Lisp(d, self.func, self.global_v, self.pre)
        return lisp.control(func)

    def call_func(self, l):
        func_name = l[0]
        param = l[1:]

        func = self.func[func_name]
        fp = func[0]
        code = func[1]

        p = self.f2a(fp, param)
        d = self.global_v.copy()
        d.update(p)
        lisp = Lisp(d, self.func, self.global_v)
        lisp.set_pre(fp)
        return lisp.control(code)
