from src.core import Core

config = {
    "source": [".\\src"],
    "source_depth": 1,
    "source_exclude_pattern": ["__init__"],
    "destination": ".\\docs\\api",
    "destination_overwrite": True,
    "graphic_md":
        {
            "footer": "Visit [Graphic Art Quest](https://www.GraphicArtQuest.com) for more!"
        }
}

core = Core(config)
core.build()