from dataclasses import dataclass

@dataclass
class Theme:
    name: str = "CodeParity"
    background: str = "#181818"
    foreground: str = "#ebdbb2"

    def describe(self) -> str:
        return f"{self.name}: {self.background}"


if __name__ == "__main__":
    print(Theme().describe())
