from dataclasses import dataclass

@dataclass
class Theme:
    name: str = "CodeParity"
    background: str = "#202124"
    foreground: str = "#d6d3c8"

    def describe(self) -> str:
        return f"{self.name}: {self.background}"


if __name__ == "__main__":
    print(Theme().describe())
