# openai_api_python
the course of openai api 

## 环境安装
### 1. 安装anaconda
```shell
https://www.anaconda.com/products/individual
```
### 2. 创建虚拟环境
```shell
conda create -n openai_api_python python=3.11
```
### 3. 激活虚拟环境
```shell
conda activate openai_api_python
```
### 4. 安装依赖
```shell
pip install -r requirements.txt
```

## OpenAI Key 准备
开了个50刀额度的token，openai的所有接口都能用，免翻墙使用。  <br/>

域名：https://key.wenwen-ai.com <br/>
key：sk-6V2exWFBSa2lmuZ7C0D773D1BaEd4fB7A1B6A0A265D550C6
```python
# 代码运行前，需要设置环境变量
import os
os.environ['OPENAI_BASE_URL'] = 'https://key.wenwen-ai.com/v1'
os.environ['OPENAI_API_KEY'] = 'sk-6V2exWFBSa2lmuZ7C0D773D1BaEd4fB7A1B6A0A265D550C6'
```