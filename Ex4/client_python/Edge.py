class Edge:
    def __init__(self, src: int,w: float, dest: int):
        self.src = src
        self.w = w
        self.dest = dest
        self.edge = (src, dest, w)

    def get_src(self) -> int:
        return self.src

    def get_dest(self) -> int:
        return self.dest

    def get_weight(self) -> float:
        return self.w

    def __str__(self) -> str:
        return f"{self.src} , {self.dest} , {self.w}"

    def __repr__(self) -> str:
        return f"{self.src} , {self.dest} , {self.w}"


