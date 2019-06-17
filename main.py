from lisp import *
from scan import *
letters = [chr(i + 97) for i in range(26)]

l1 = ['(define y 10)',
      '(define f (lambda (x y) (+ x ((lambda (x) (* x y)) y))))',
      '(f 1 2)',
      'y']

# 样例2
l2 = ['(define y 10)',
      '(define sqr+y (lambda (x) (+ y (* x x))))',
      '(define f (lambda (x y) (sqr+y x)))',
      '(sqr+y 5)',
      '(f 5 1)']

# 样例3
l3 = ['(define fact (lambda (n) (cond ((eq? n 1) 1) (True (* n (fact (- n 1)))))))',
      '(fact 1)',
      '(fact 5)',
      '(fact 10)',
      '(define sum (lambda (n) (cond ((eq? n 1) 1) (True (+ n (sum (- n 1)))))))',
      '(sum 50)']

# 样例4
l4 = ['(define fun1 (lambda (x) (cond ((eq? x 0) 1) (True (fun2 (- x 1))))))',
      '(define fun2 (lambda (x) (cond ((eq? x 0) 2) (True (fun1 (/ x 2))))))',
      '(fun1 2)',
      '(fun2 2)',
      '(fun1 5)',
      '(fun2 5)']


if __name__ == '__main__':
    lisp = Lisp()
    form_list = []

    for i, e in enumerate(l1):
        l = parse(e)
        a = lisp.control(l)
        form_list.append(get(a))
    for i, e in enumerate(form_list):
        print(e.value)
        print(e.kind)




