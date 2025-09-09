import os
import sys

def validate_ip(ip):
    """验证IP地址格式是否正确"""
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    try:
        for part in parts:
            num = int(part)
            if num < 0 or num > 255:
                return False
        return True
    except ValueError:
        return False

def expand_ip_range(ip_range):
    try:
        # 分割起始和结束IP
        start_ip, end_ip = ip_range.split('-')
        
        # 检查是否为完整的IP地址格式
        if '.' in end_ip:
            # 格式2: 192.168.1.1-192.168.1.255
            if not (validate_ip(start_ip) and validate_ip(end_ip)):
                return "无效的IP地址格式！请确保起始和结束IP都是有效的IPv4地址。"
            
            # 解析起始IP和结束IP的各段
            start_parts = list(map(int, start_ip.split('.')))
            end_parts = list(map(int, end_ip.split('.')))
            
            # 验证IP范围的有效性
            # 目前只支持最后一段不同的情况，如192.168.1.1-192.168.1.255
            if start_parts[:3] != end_parts[:3] or start_parts[3] > end_parts[3]:
                return "无效的IP范围！目前只支持同一子网的连续IP范围。"
            
            # 生成IP列表
            prefix = '.'.join(map(str, start_parts[:3]))
            ip_list = [f"{prefix}.{num}" for num in range(start_parts[3], end_parts[3] + 1)]
        else:
            # 格式1: 192.168.1.1-255
            if not validate_ip(start_ip):
                return "无效的起始IP地址格式！"
            
            # 解析起始IP的前三个段
            prefix = '.'.join(start_ip.split('.')[:-1])
            # 获取起始IP的最后一段数字
            start_num = int(start_ip.split('.')[-1])
            # 获取结束IP的数字
            end_num = int(end_ip)
            
            # 验证范围有效性
            if start_num < 0 or end_num > 255 or start_num > end_num:
                return "无效的IP范围！请确保起始值小于结束值，且都在0-255之间。"
            
            # 生成IP列表
            ip_list = [f"{prefix}.{num}" for num in range(start_num, end_num + 1)]
        
        return '\n'.join(ip_list)
    except ValueError:
        return "格式错误！请使用类似'192.168.1.1-255'或'192.168.1.1-192.168.1.255'的格式。"
    except Exception as e:
        return f"发生错误：{str(e)}"

def process_file(file_path):
    """处理文件中的IP范围，每行一个范围"""
    try:
        if not os.path.exists(file_path):
            return "文件不存在！"
        
        all_ips = []  # 存储所有有效的IP地址
        error_messages = []  # 存储错误信息
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line:  # 跳过空行
                continue
            
            result = expand_ip_range(line)
            if result.startswith("无效") or result.startswith("格式错误") or result.startswith("发生错误"):
                error_messages.append(f"第{i}行 ({line}): {result}")
            else:
                # 将IP地址添加到列表中，使用换行符分隔
                all_ips.extend(result.split('\n'))
        
        # 首先输出所有错误信息（如果有）
        output = []
        if error_messages:
            output.append('\n'.join(error_messages))
            if all_ips:  # 如果同时有错误信息和有效IP，添加一个空行分隔
                output.append('')
        
        # 然后输出所有有效IP，用换行符连接
        output.append('\n'.join(all_ips))
        
        return '\n'.join(output)
    except Exception as e:
        return f"处理文件时发生错误：{str(e)}"

def main():
    """主函数，处理命令行参数"""
    
    # 检查命令行参数
    if len(sys.argv) < 2:
        # 显示帮助手册
        print("IP地址范围扩展工具")
        print("使用方法：")
        print("  python IP_EXPAND.py <IP范围或文件路径> [--out]")
        print("示例：")
        print("  python IP_EXPAND.py 192.168.1.1-20")
        print("  python IP_EXPAND.py ip.txt")
        print("  python IP_EXPAND.py 192.168.1.1-20 --out")
        sys.exit(1)
    
    # 获取输入内容
    user_input = sys.argv[1]
    # 检查是否需要输出到文件
    output_to_file = len(sys.argv) > 2 and sys.argv[2] == "--out"
    
    # 智能检测是否为文件路径
    if os.path.isfile(user_input):
        print(f"检测到文件路径，正在处理文件：{user_input}")
        result = process_file(user_input)
    elif user_input.lower().startswith('file:'):
        # 保持向后兼容性，支持原来的file:前缀格式
        file_path = user_input[5:].strip()
        print(f"正在处理文件：{file_path}")
        result = process_file(file_path)
    else:
        # 扩展并输出结果
        result = expand_ip_range(user_input)
    
    # 输出结果
    if output_to_file:
        try:
            with open('res.txt', 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"处理结果已保存到res.txt文件中")
        except Exception as e:
            print(f"保存结果到文件时出错：{str(e)}")
            print("处理结果：")
            print(result)
    else:
        print("处理结果：")
        print(result)

if __name__ == "__main__":
    main()
    