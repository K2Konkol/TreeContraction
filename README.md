Tree contraction evaluation example:

```sh
# TreeContraction.py
# line 322

    expression = "((2+3)·2)+((4·2)+2)"
```

Example output:

```sh
Expression: ((2+3)·2)+((4·2)+2)
------------------
[2, 3, +, 2, *, 4, 2, *, 2, +, +]
------------------

A = [3, 2, 4, 2]

----------
Iteration 1
----------

(1)

A_odd = [3, 4]
A_even = [2, 2]

(2a)
Left child

*** Rake ***
Operation: (*)
Node value = 4
(A_u, B_u)           = (1, 0)
(A_v, B_v)           = (1, 0)
(A_w, B_w)           = (1, 0)
(A_prim_w, B_prim_w) = (4, 0)
        
A_odd = [3]

(2b)

Right child

*** Rake ***
Operation: (+)
Node value = 3
(A_u, B_u)           = (1, 0)
(A_v, B_v)           = (1, 0)
(A_w, B_w)           = (1, 0)
(A_prim_w, B_prim_w) = (1, 3)
        
(2c)

A = [2, 2]

----------
Iteration 2
----------

(1)

A_odd = [2]
A_even = [2]

(2a)
A_odd = [2]

(2b)

Right child

*** Rake ***
Operation: (*)
Node value = 2
(A_u, B_u)           = (1, 0)
(A_v, B_v)           = (1, 0)
(A_w, B_w)           = (1, 3)
(A_prim_w, B_prim_w) = (2, 6)
        
(2c)

A = [2]

----------
Iteration 3
----------

(1)

A_odd = [2]
A_even = []

(2a)
Left child

*** Rake ***
Operation: (+)
Node value = 2
(A_u, B_u)           = (1, 0)
(A_v, B_v)           = (4, 0)
(A_w, B_w)           = (1, 0)
(A_prim_w, B_prim_w) = (1, 8)
        
A_odd = []

(2b)

(2c)

Two remaining nodes: ('2', 2, 6), ('2', 1, 8)
Note: check above which one is left and which is right

Score = 10 + 10 = 20
```
