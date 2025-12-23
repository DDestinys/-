#!/usr/bin/env python3
"""
文本行数拆分工具
将一个大文件按指定行数拆分成多个小文件
"""

import argparse
import os
import sys

def split_file(input_file, lines_per_file, output_prefix=None):
    """
    拆分文件
    
    Args:
        input_file: 输入文件路径
        lines_per_file: 每个输出文件的行数
        output_prefix: 输出文件前缀（默认为输入文件名）
    """
    # 检查文件是否存在
    if not os.path.exists(input_file):
        print(f"错误: 文件 '{input_file}' 不存在")
        sys.exit(1)
    
    # 获取输入文件名（不含扩展名）
    if output_prefix is None:
        base_name = os.path.splitext(os.path.basename(input_file))[0]
    else:
        base_name = output_prefix
    
    # 统计总行数
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            total_lines = sum(1 for _ in f)
    except UnicodeDecodeError:
        # 如果utf-8失败，尝试其他编码
        try:
            with open(input_file, 'r', encoding='gbk') as f:
                total_lines = sum(1 for _ in f)
        except:
            with open(input_file, 'r', encoding='latin-1') as f:
                total_lines = sum(1 for _ in f)
    
    print(f"总行数: {total_lines}")
    
    # 计算需要拆分成几个文件
    num_files = (total_lines + lines_per_file - 1) // lines_per_file
    print(f"将拆分成 {num_files} 个文件，每个文件 {lines_per_file} 行")
    
    # 开始拆分
    file_count = 0
    line_count = 0
    
    try:
        # 尝试utf-8编码打开
        input_f = open(input_file, 'r', encoding='utf-8')
    except UnicodeDecodeError:
        try:
            # 尝试gbk编码
            input_f = open(input_file, 'r', encoding='gbk')
        except:
            # 尝试latin-1编码
            input_f = open(input_file, 'r', encoding='latin-1')
    
    current_file = None
    
    try:
        for line_num, line in enumerate(input_f, 1):
            # 如果是新文件的开始
            if line_count == 0:
                file_count += 1
                output_filename = f"{base_name}_part{file_count:03d}.txt"
                current_file = open(output_filename, 'w', encoding='utf-8')
                print(f"创建文件: {output_filename}")
            
            # 写入行
            current_file.write(line)
            line_count += 1
            
            # 如果达到指定行数，关闭当前文件
            if line_count == lines_per_file:
                current_file.close()
                line_count = 0
                
                # 显示进度
                percent = min(100, (line_num / total_lines) * 100)
                print(f"进度: {line_num}/{total_lines} ({percent:.1f}%)")
        
        # 如果有未关闭的文件，关闭它
        if current_file and not current_file.closed:
            current_file.close()
        
        input_f.close()
        
        print(f"\n拆分完成!")
        print(f"共生成 {file_count} 个文件")
        
        # 显示生成的文件列表
        print(f"\n生成的文件:")
        for i in range(1, file_count + 1):
            filename = f"{base_name}_part{i:03d}.txt"
            # 统计每个文件的行数
            with open(filename, 'r', encoding='utf-8') as f:
                part_lines = sum(1 for _ in f)
            print(f"  {filename}: {part_lines} 行")
        
    except Exception as e:
        print(f"拆分过程中出错: {e}")
        if current_file and not current_file.closed:
            current_file.close()
        if input_f and not input_f.closed:
            input_f.close()
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='文本文件行数拆分工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s input.txt 5000           # 将input.txt按每5000行拆分
  %(prog)s input.txt 1000 -p split  # 拆分并指定输出文件前缀
  %(prog)s -i input.txt -l 2000     # 另一种参数格式
  
示例场景:
  10000行的文件拆分成2个5000行的文件:
    %(prog)s large_file.txt 5000
    -> 生成: large_file_part001.txt (5000行)
        large_file_part002.txt (5000行)
        
  12345行的文件拆分成每3000行:
    %(prog)s data.txt 3000
    -> 生成5个文件: 3000+3000+3000+3000+345行
        """
    )
    
    # 两种参数格式都支持
    parser.add_argument('input_file', nargs='?', help='输入文件路径')
    parser.add_argument('lines', nargs='?', type=int, help='每个文件的行数')
    
    parser.add_argument('-i', '--input', help='输入文件路径')
    parser.add_argument('-l', '--lines', type=int, help='每个文件的行数')
    parser.add_argument('-p', '--prefix', help='输出文件前缀')
    
    args = parser.parse_args()
    
    # 处理参数
    input_file = args.input or args.input_file
    lines_per_file = args.lines or args.lines
    
    if not input_file:
        print("错误: 请指定输入文件")
        parser.print_help()
        sys.exit(1)
    
    if not lines_per_file or lines_per_file <= 0:
        print("错误: 请指定有效的行数（大于0）")
        parser.print_help()
        sys.exit(1)
    
    print(f"文件: {input_file}")
    print(f"每文件行数: {lines_per_file}")
    print("-" * 40)
    
    split_file(input_file, lines_per_file, args.prefix)

if __name__ == "__main__":
    main()