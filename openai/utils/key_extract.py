def main():
    keys_35 = []

    # 读取keys.txt文件中的key
    with open('keys-0415.txt', 'r') as file:
        keys = file.readlines()
        # 循环遍历每个key
        for key in keys:
            # 解析 'sk-' 开头的 key， Glenn_Jackson_869829@outlook.com----cBubpkuG3tYpuq----U99bo3uQIygc----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----
            k = key.split("----")[3]
            keys_35.append(k)
            print(f"{k}")
    return keys_35[0]


# main
if __name__ == "__main__":
    main()
