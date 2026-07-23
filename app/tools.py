from __future__ import annotations

from langchain.tools import tool

@tool
def add(a: int, b: int) -> int:
    """计算两个整数的加法，只能用于求和运算
    Args:
        a: 整型数字，加法第一个加数
        b: 整型数字，加法第二个加数
    """
    return a + b

@tool
def subtract(a:int, b:int) -> int:
    """计算两数相减
    Args:
        a：减数1
        b：减数2
    """
    return a - b

@tool
def multiply(a: int, b: int) -> int:
    """计算两个数字相乘
    Args:
        a: 乘数1
        b: 乘数2
    """
    return a * b


@tool
def divide(a: int, b: int):
    """计算两个数字相乘
    Args:
        a: 被除数1
        b: 除数2
    """
    if b == 0:
        return 0
    return a / b

