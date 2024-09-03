class Content:
    def __init__(self, data: dict[str, str]) -> None:
        self.type: str = data.get("type", "No Type")
        self.code: str = data.get("code", "No Code")
    
    def __repr__(self):
        return f"Content(type={self.type}, code={self.code})"

class Map:
    def __init__(self, data: dict[str, str | int]) -> None:
        self.name: str = data.get("name", "No Name")
        self.skin: str = data.get("skin", "No Skin")
        self.x: int = data.get("x", 0)
        self.y: int = data.get("y", 0)
        self.content: None | Content = (Content(data.get("content")) if data.get("content") else None)
    
    def __repr__(self):
        return (
            f"Map(name={self.name}, skin={self.skin}, x={self.x}, y={self.y}, content={self.content})"
        )