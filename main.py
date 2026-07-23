from app.graph import get_result

# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    input = "计算 123456加上789012再乘上3000再减100再除100"
    result = get_result(input)
    print(result)


