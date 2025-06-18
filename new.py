import getpass
import os
import re
import chardet

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.document_loaders import TextLoader

os.environ["OPENAI_API_KEY"] = "sk-kTtVqDFBwOc4coa2HKva2rlSmHVufJ07FgL6uilOScGMT6Uc"
os.environ["OPENAI_BASE_URL"] = "https://api.chatanywhere.tech"

model = ChatOpenAI(model="gpt-4o-mini")


# 返回字典对象
def file_loader(file_name: str):
    loader = TextLoader(file_name, encoding="utf-8")
    documents = loader.load()
    code = documents[0].page_content
    return {"file_name": file_name, "content": code}


def detect_file_encoding(file_path, sample_size=10000):
    with open(file_path, "rb") as f:
        raw_data = f.read(sample_size)  # 读取前10KB用于检测
    result = chardet.detect(raw_data)
    return result["encoding"], result["confidence"]


def add_line_numbers_to_string(file):
    lines = file.split("\n")

    modified_content = ""
    for idx, line in enumerate(lines, start=1):
        # 添加行号信息并追加到modified_content字符串变量中
        modified_line = f"{line.rstrip()}  # 第{idx}行\n"
        modified_content += modified_line
    return modified_content  # 返回包含行号的新字符串内容


def delete_line(text, start, end):
    # 将文本按行分割成列表
    lines = text.splitlines()

    # 删除指定行（注意索引从0开始)
    delete_line_nums = end - start + 1
    for i in range(delete_line_nums):
        lines.pop(start - 1)

    # 重新组合成单个字符串
    modified_text = "\n".join(lines)

    return modified_text


def add_line(text, start, insert_content):
    # 将文本按行分割成列表
    lines = text.splitlines()

    # 插入新内容到指定行前
    if 1 <= start <= len(lines) + 1:
        lines.insert(start - 1, insert_content)

    # 重新组合成单个字符串
    modified_text = "\n".join(lines)

    return modified_text


def code_extract(llm_code: str):
    pattern = r"(.*?)```"
    match = re.search(pattern, llm_code, re.DOTALL)
    if match:
        before_code_block = match.group(1).strip()

        # extract code
        code_pattern = r"```(?:\w+)?(.*?)(?:```|$)"
        code_match = re.search(code_pattern, llm_code, re.DOTALL)
        if code_match:
            code_block = code_match.group(1).strip()
            print(code_block)
            return code_block
    else:
        return llm_code


if __name__ == "__main__":
    # problem = "这段代码统计学生平均分数逻辑错了。"+"帮我修改，只需要输出需要改进的代码结果"
    problem = "这段代码缺少一个统计单个学生平均成绩的功能，帮我添加。这段代码的add_grade方法    可读性差，帮我修改。这段代码有一个重复的功能，帮我删除。"
    problem = (
        problem
        + "只需要输出需要改动的代码，不需要输出全部代码。每个问题都要输出思考过程"
    )
    code = file_loader("./buggy.py")["content"]
    msg = HumanMessage(content=code + problem)
    resp = model.invoke([msg])
    print(resp.content)
