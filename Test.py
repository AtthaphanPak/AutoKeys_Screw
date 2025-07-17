import os
path = "C:\ProgramData\Atlas Copco\LBConfigurator\singlequalitysolution\9d196b0464c56e3b9c92ab4ddf0f4454\stations\CUS-2163-031"
full_path = os.path.join(path, "test.txt")
print(full_path)
with open(full_path, "w", encoding="utf-8") as f:
    # f.write("HELLO WORLD")
    pass
