class escapesequences:
    def HOME(self):
        print("\033[H", end="")
    def CLEAR(self):
        print("\033[2J", end="")