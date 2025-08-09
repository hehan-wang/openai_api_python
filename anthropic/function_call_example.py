import json
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY", "sk-6V2exWFBSa2lmuZ7C0D773D1BaEd4fB7A1B6A0A265D550C6"),
    base_url=os.getenv("ANTHROPIC_BASE_URL", "https://api.wenwen-ai.com")
)

def get_weather(location: str) -> dict:
    """模拟获取天气信息的函数"""
    weather_data = {
        "北京": {"temperature": "25°C", "condition": "晴天", "humidity": "60%"},
        "上海": {"temperature": "28°C", "condition": "多云", "humidity": "70%"},
        "广州": {"temperature": "32°C", "condition": "雨天", "humidity": "85%"},
    }
    return weather_data.get(location, {"error": "找不到该城市的天气信息"})

def calculate(operation: str, a: float, b: float) -> float:
    """执行基本数学运算"""
    operations = {
        "add": a + b,
        "subtract": a - b,
        "multiply": a * b,
        "divide": a / b if b != 0 else "除数不能为零"
    }
    return operations.get(operation, "不支持的运算")

tools = [
    {
        "name": "get_weather",
        "description": "获取指定城市的天气信息",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "城市名称，例如：北京、上海、广州"
                }
            },
            "required": ["location"]
        }
    },
    {
        "name": "calculate",
        "description": "执行基本的数学运算",
        "input_schema": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"],
                    "description": "要执行的运算类型"
                },
                "a": {
                    "type": "number",
                    "description": "第一个数字"
                },
                "b": {
                    "type": "number", 
                    "description": "第二个数字"
                }
            },
            "required": ["operation", "a", "b"]
        }
    }
]

def handle_function_call(message):
    """处理函数调用"""
    if message.type == "tool_use":
        tool_name = message.name
        tool_input = message.input
        
        if tool_name == "get_weather":
            result = get_weather(tool_input["location"])
        elif tool_name == "calculate":
            result = calculate(tool_input["operation"], tool_input["a"], tool_input["b"])
        else:
            result = {"error": f"未知的工具: {tool_name}"}
        
        return {
            "type": "tool_result",
            "tool_use_id": message.id,
            "content": json.dumps(result, ensure_ascii=False)
        }
    
    return None

def chat_with_tools(user_message: str):
    """与Claude进行工具增强的对话"""
    messages = [{"role": "user", "content": user_message}]
    
    response = client.messages.create(
        # model="claude-sonnet-4-20250514",
        model="claude-3-7-sonnet-20250219",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )
    
    print(f"用户: {user_message}")
    
    # 检查是否有工具调用
    if any(block.type == "tool_use" for block in response.content):
        # 处理工具调用
        tool_results = []
        assistant_message_content = []
        
        for block in response.content:
            if block.type == "text":
                assistant_message_content.append({"type": "text", "text": block.text})
                print(f"Claude: {block.text}")
            elif block.type == "tool_use":
                assistant_message_content.append({
                    "type": "tool_use",
                    "id": block.id,
                    "name": block.name,
                    "input": block.input
                })
                
                # 执行工具调用
                tool_result = handle_function_call(block)
                tool_results.append(tool_result)
                print(f"工具调用: {block.name} - 参数: {block.input}")
                print(f"工具结果: {tool_result['content']}")
        
        # 如果有工具调用结果，继续对话获取最终回复
        if tool_results:
            messages.append({"role": "assistant", "content": assistant_message_content})
            messages.append({"role": "user", "content": tool_results})
            
            final_response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                tools=tools,
                messages=messages
            )
            
            for block in final_response.content:
                if block.type == "text":
                    print(f"Claude最终回复: {block.text}")
    
    else:
        # 没有工具调用，直接显示回复
        for block in response.content:
            if block.type == "text":
                print(f"Claude: {block.text}")

if __name__ == "__main__":
    # 示例对话
    examples = [
        "北京的天气怎么样？"
        # ,"计算 15 加 27 等于多少",
        # "上海今天的天气如何？",
        # "帮我计算 100 除以 4",
        # "你好，请介绍一下自己"
    ]
    
    print("=== Anthropic Function Calling 示例 ===\n")
    
    for i, example in enumerate(examples, 1):
        print(f"--- 示例 {i} ---")
        chat_with_tools(example)
        print()