import re


def remove_middle_dot(input_str):
    return re.sub('·', '*', input_str)


def infix_to_postfix(input_expr):
    prec: dict = {
        "*": 3,
        "+": 2,
        "(": 1
    }
    operators_stack = []
    postfix_list = []
    """
    wersja alternatywna jeśli wejście ma być ze spacjami:
    expression = "( ( ( ( ( 4 + 5 ) * 2 ) + ( 2 + ( -5 ) ) ) * 2 ) + 2 )"
    token_list = (remove_middle_dot(input_expr)).split()
    """

    token_list = list((remove_middle_dot(input_expr)))

    for token in token_list:
        if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or token in "-0123456789":
            postfix_list.append(token)
        elif token == '(':
            operators_stack.append(token)
        elif token == ')':
            top_token = operators_stack.pop()
            while top_token != '(':
                postfix_list.append(top_token)
                top_token = operators_stack.pop()
        elif token == ' ':
            pass
        else:
            while (len(operators_stack) != 0) and (prec[operators_stack[-1]] >= prec[token]):
                postfix_list.append(operators_stack.pop())
            operators_stack.append(token)

    while len(operators_stack) != 0:
        postfix_list.append(operators_stack.pop())
    return postfix_list
