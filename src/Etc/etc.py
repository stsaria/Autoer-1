def input_yes_no(text):
    """y/nの確認するための関数"""
    while True:
        choice = input(text)
        if choice in ["yes", "ye", "y"]:
            return True
        if choice in ["no", "n"]:
            return False