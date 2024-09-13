import tkinter as tk
from tkinter import filedialog
import os
import re
import yaml
import openai

def get_filepath():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    default_dir = os.getenv('OB_VAULT_DIR')
    
    filepath = filedialog.askopenfilename(
        initialdir=default_dir,
        title="选择文件",
        filetypes=(("Markdown files", "*.md"), ("所有文件", "*.*"))
    )
    
    return filepath if filepath else None

def translate_filename(filename):
    # 从环境变量获取 Azure OpenAI 配置
    openai.api_type = "azure"
    openai.api_base = os.getenv("AZURE_OPENAI_API_BASE")
    openai.api_version = "2023-05-15"
    openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")

    # 移除文件扩展名进行翻译
    name_without_ext = os.path.splitext(filename)[0]
    
    try:
        response = openai.ChatCompletion.create(
            engine=os.getenv("AZURE_OPENAI_MODEL_NAME"),
            messages=[
                {"role": "system", "content": "你是一个文件名翻译助手。请将给定的中文文件名翻译成简洁的英文，不超过50个字符，并使用下划线连接单词。"},
                {"role": "user", "content": f"请翻译以下文件名：{name_without_ext}"}
            ],
            max_tokens=60
        )
        
        translated_filename = response['choices'][0]['message']['content'].strip()
        
        # 将翻译结果转换为合法的文件名
        translated_filename = re.sub(r'[^\w\-_\. ]', '', translated_filename)
        translated_filename = translated_filename.replace(' ', '_').lower()
        
        # 确保文件名不超过50个字符
        if len(translated_filename) > 50:
            translated_filename = translated_filename[:50]
        
        return translated_filename + '.md'
    except Exception as e:
        print(f"翻译出错: {e}")
        return filename  # 如果翻译失败，返回原始文件名

def create_new_md_file(original_filepath, translated_filename):
    # 读取原始文件内容
    with open(original_filepath, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    # 解析原始文件的front matter
    if original_content.startswith('---'):
        _, original_front_matter, original_body = original_content.split('---', 2)
        original_front_matter = yaml.safe_load(original_front_matter)
    else:
        original_front_matter = {}
        original_body = original_content
    
    # 获取原始文件名（不包含扩展名）作为标题
    original_title = os.path.splitext(os.path.basename(original_filepath))[0]
    
    # 获取子目录作为分类
    relative_path = os.path.relpath(original_filepath, os.getenv('OB_VAULT_DIR'))
    categories = os.path.dirname(relative_path).split(os.sep)
    categories = [cat for cat in categories if cat]  # 移除空字符串
    
    # 更新front matter
    front_matter = original_front_matter
    front_matter['title'] = original_title
    front_matter['categories'] = categories
    
    # 将front matter转换为YAML格式
    yaml_front_matter = yaml.dump(front_matter, allow_unicode=True)
    
    # 创建新的Markdown文件内容
    new_content = f"---\n{yaml_front_matter}---\n\n{original_body.strip()}"
    
    # 获取输出目录
    output_dir = get_output_directory()
    
    # 写入新文件
    new_filepath = os.path.join(output_dir, translated_filename)
    with open(new_filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return new_filepath
def get_output_directory():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    default_dir = os.getenv('HUGO_POST_DIR')
    
    output_dir = filedialog.askdirectory(
        initialdir=default_dir,
        title="选择新文件保存目录"
    )
    
    return output_dir if output_dir else default_dir

# 测试函数
if __name__ == "__main__":
    selected_filepath = get_filepath()
    if selected_filepath:
        original_filename = os.path.basename(selected_filepath)
        print(f"选择的文件路径: {selected_filepath}")
        print(f"原始文件名: {original_filename}")
        
        translated_filename = translate_filename(original_filename)
        print(f"翻译后的文件名: {translated_filename}")
        
        new_filepath = create_new_md_file(selected_filepath, translated_filename)
        print(f"新创建的文件路径: {new_filepath}")
    else:
        print("未选择文件")