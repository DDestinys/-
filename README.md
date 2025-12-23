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
