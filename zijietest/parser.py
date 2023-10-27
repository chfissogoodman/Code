import time
import json

from pyparsing import *
from datetime import datetime

def get_parser():
    LBRA, RBRA, LPAREN, RPAREN, COLON, SEMI, QUOTE, COMMA = map(Suppress, '{}():;",')
    B_SLASH = Suppress("\\")
    voltage_names = ['VDD', 'VSS', 'AVDD', 'AVSS', 'VDDL', 'VSSL']
    COMMENT_START = Literal("/*").suppress()
    COMMENT_END = Literal("*/").suppress()
    STRING = Literal("STRING")

    boolean = Group(CaselessKeyword('true') | CaselessKeyword('false') | CaselessKeyword('TRUE') | CaselessKeyword('FALSE'))('boolean')
    number = Word(nums + '.')
    integer = Group(number + Optional(~Literal('.') + number))('integer')
    float_number = Group(number + Optional(Literal('.') + number))('float')

    expr_number = Word(nums + '+' + "-" + "*", nums + ".")
    symbol = Word("+-*/")
    voltage_value = Word(" ".join(voltage_names))

    date = Group(QUOTE + Regex(r'\d{4}/\d{2}/\d{2}, \d{2}:\d{2}:\d{2}').setParseAction(lambda s: datetime.strptime(s[0], '%Y/%m/%d, %H:%M:%S')) + QUOTE)('date')

    identifier = Group(Word(init_chars=alphas + "_", body_chars=alphanums + "_[]" + "."))('identify')
    comlpex_value = Group(Word(init_chars=alphas + "_", body_chars=alphanums + "_[]" + "." + "[" + "]" + ":"))
    string = Group(QUOTE + Regex(r'[^"]*') + QUOTE)('string')
    expr_value = Group((expr_number + symbol + voltage_value) | (voltage_value + symbol + expr_number) | expr_number)
    anno_value = Group(COMMENT_START + identifier + COMMENT_END)

    STRING_value = Group(STRING + delimitedList(identifier) + STRING + identifier + identifier)

    value = expr_value | comlpex_value |  integer | float_number | boolean | date | string | identifier

    # tuple_list_value = Group(value + COMMA + value + Optional(COMMA + value))
    tuple_list_value = Group(delimitedList(value, ","))

    value_str = Group(Optional(B_SLASH) + QUOTE + delimitedList(float_number) + QUOTE + Optional(B_SLASH))
    tuple_list_string_value = Group(delimitedList(value_str, ','))

    condition = Group(identifier + LPAREN + Optional(tuple_list_string_value | tuple_list_value) + RPAREN + SEMI)
    dict_value = Group(identifier + COLON + Optional(value) + SEMI)
    entry = condition | dict_value | anno_value | STRING_value

    block = Forward()
    block_body = Group(ZeroOrMore(entry | block))
    block << Group(identifier + LPAREN + Optional(value)  + RPAREN + LBRA + block_body + RBRA)
    parser = ZeroOrMore(entry | block).ignore(cppStyleComment)
    return parser

def process(element):
        processed_data = {}
        
        
        if isinstance(element, datetime):
            element = element.strftime('%Y-%m-%d %H:%M:%S')
        
        if not isinstance(element, list):
            if isinstance(element, str):
                if element.lower() == "true":
                    element = True
                elif element.lower() == "false":
                    element = False
                elif "." in element:
                    try:
                        element = float(element)
                    except:
                        pass
                else:
                    try:
                        element = int(element)
                    except:
                        pass
            return element
        else:
            if all(map(lambda x: isinstance(x, str), element)):
                try:
                    return list(map(lambda x: float(x), element))
                except:
                    if len(element) == 1:
                        return element[0]
                    return element
            elif len(element) > 3 and all(map(lambda x: len(x) == 1, element)) and all(map(lambda x: isinstance(x[0], str), element)):
                try:
                    return list(map(lambda x: float(x[0]), element))
                except:
                    return list(map(lambda x: x[0], element))
        
        if len(element) == 1:
            return process(element[0])
        
        if (len(element) == 3 or len(element) == 2) and \
        (len(element[0]) == 1 and isinstance(element[0][0], str)):
            
            # pprint.pprint(element)
            # print("*" * 100)
            
            key = element[0][0]
            if len(element) == 3:
                
                
                
                for data in element[-1]:
                    
                    if len(data) > 1:
                        if len(data[1]) == 2:
                            if all(map(lambda x: isinstance(x[0], str), data[1])):
                                data = [data[0], *data[1]]
                    
                    value = process(data)
                    
                    if not isinstance(element[1][0], str):
                        element[1][0] = element[1][0][0]
                    
                    if not processed_data.get(key):
                        processed_data[key] = {element[1][0]: value}
                    else:
                        
                        # 检查当前value中的键是否已经存在于processed_data中
                        current_dict = processed_data[key][element[1][0]]
                        current_value_first_key = list(value.keys())[0]
                        current_value_first_value = list(value.values())[0]
                        
                        if current_dict.get(current_value_first_key):
                            
                            # 若存在，且value为dict，则把value的dict更新到processed_data内
                            if isinstance(current_dict.get(current_value_first_key), dict):
                                
                                if current_value_first_value.keys() == current_dict[current_value_first_key].keys():
                                    
                                    if not isinstance(current_dict[current_value_first_key], list):
                                        
                                        current_dict[current_value_first_key] = [current_dict[current_value_first_key]]
                                        current_dict[current_value_first_key].append(current_value_first_value)
                                    
                                    else:
                                        current_dict[current_value_first_key].append(current_value_first_value)
                                else:
                                    current_dict[current_value_first_key].update(current_value_first_value)
                            else:
                                if not isinstance(current_dict.get(current_value_first_key), list):
                                    current_dict[current_value_first_key] = [current_dict[current_value_first_key]] 
                                    current_dict[current_value_first_key].append(current_value_first_value)
                                else:

                                    if not isinstance(current_value_first_value, list):
                                        current_dict[current_value_first_key].append(current_value_first_value)
                                    else:
                                        current_dict[current_value_first_key].extend(current_value_first_value)
                        else:
                            current_dict.update(value)
                    
                    
                return processed_data
            else:


                if len(element[-1]) > 1:
                    if isinstance(element[-1][0], str):
                        element[-1] = [" ".join(element[-1])]
                    elif all(map(lambda x: len(x) == 1, element[-1])):
                        element[-1] = [list(map(lambda x: x[0], element[-1]))]
                for data in element[-1]:
                    
                    value = process(data)
                    
                    if not processed_data.get(key):
                        processed_data[key] = value
                    else:
                        if not isinstance(value, dict):
                            if not isinstance(processed_data[key], list):
                                processed_data[key] = [value]
                            else:
                                processed_data[key].extend(value)
                        else:
                            processed_data[key].update(value)

                return processed_data
        elif len(element[0]) != 1:
            while len(element) != 1 and len(element[0]) != 1:
                key = element[0][0]
                if not processed_data.get(key):
                    processed_data[key] = []
                values = []
                for data in element[0]:
                    if data == key:
                        continue
                    values.append(data)
                processed_data[key].append(values)
                element.remove(element[0])
            value = process(element)
            processed_data.update(value)
        
        return processed_data
        

class LibReader:
    
    def __init__(self, path: str) -> None:
        with open(path, "r") as f:
            self.text = f.read()
        self.parser = get_parser()
            
            
    def parse(self):
        res = self.parser.parseString(self.text).as_list()      
        return res
    
    def json(self):
        
        data = self.parse()
        dict_data = process(data)          
        
        return json.dumps(dict_data, indent=4)
    
if __name__ == "__main__":
    import pprint
    
    # 这里填写需要解析的文件路径, 解析完成的文件将保存至原路径
    file_path = "/home/chen/CLionProjects/zijietest/test.txt"
    # file_path = "./lib_parser/ram1kx32_2p1r1w.lib"
    # file_path = "./lib_parser/test.txt"
    
    reader = LibReader(file_path)

    with open(file_path[:-4] + ".json", "w") as f:
        f.write(reader.json())

