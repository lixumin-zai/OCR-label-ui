import re


# <text> A: 69. </text> <blank> <handwritten> <del> How $y=kx^2+b$ </del> How long do you usually get there $y=kx+b$ </handwritten> </blank> <text> ? </text>
# <text> A: 69. </text> <u> <span style="color: red;"> <del> How </del> How long do you usually get there $y=kx+b$</span> </u> <text> ? </text>
def xizhi_text2latex(text):
    pass


# <text> A: 69. </text> <blank> <handwritten> <del> How $y=kx^2+b$ </del> How long do you usually get there $y=kx+b$ </handwritten> </blank>
# <text></text> 文本正常提取
# <blank></blank>包裹的文本使用\underline{}包裹
# <del></del>  包裹的文本如果里含有$$包裹的公式，则将公式使用 $\enclose{horizontalstrike}{}$包裹
# <handwritten> </handwritten>替换为<span style="color: red;"><span>,如果文本里包含$$包裹的公式，则使用$\textcolor{red}{}$包裹
# 注意他们可能相互嵌套

import re

def process_text(text):
    # Step 1: Handle <blank> tags
    text = re.sub(r'<blank>(.*?)</blank>', r'\\underline{\1}', text)
    def handle_handwritten(match):
        content = match.group(1)
        if "$" in content:  # Check if there's a $$ formula
            content = re.sub(r'\$(.*?)\$', r'$\\textcolor{red}{\1}$', content)
        return r'<span style="color: red;">' + content + r'</span>'
    text = re.sub(r'<handwritten>(.*?)</handwritten>', handle_handwritten, text)


    def handle_del(match):
        content = match.group(1)
        if "$" in content:  # Check if there's a $$ formula
            # Remove $$ and apply horizontal strike to the formula inside
            content = re.sub(r'\$(.*?)\$', r'$\\enclose{horizontalstrike}{\1}$', content)
        return "<del>" + content + "</del>"
    text = re.sub(r'<del>(.*?)</del>', handle_del, text)

    return text


# Example input string
input_text = r"<text> A: 69. </text> <blank> <handwritten> <del> How $y=kx^2+b$ </del> How long do you usually get there $y=kx+b$ </handwritten> </blank> <handwritten>21342</handwritten>"

# Process the text
output_text = process_text(input_text)
print(output_text)

# <blank><handwritten><text><del></del></text></handwritten></blank> 优先级最大
