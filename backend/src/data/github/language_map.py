import json
import urllib.request
from typing import Any, Dict

BLACKLIST = [".md"]

with urllib.request.urlopen(
    "https://raw.githubusercontent.com/blakeembrey/language-map/main/languages.json"
) as url:
    data: Dict[str, Dict[str, Any]] = json.loads(url.read().decode())
    languages = {
        k: v
        for k, v in data.items()
        if v["type"] in ["programming", "markup"] and "color" in v and "extensions" in v
    }
    extensions: Dict[str, Dict[str, str]] = {}
    for lang_name, lang in languages.items():
        for extension in lang["extensions"]:
            if extension not in BLACKLIST:
                extensions[extension] = {"color": lang["color"], "name": lang_name}
    extensions = dict(sorted(extensions.items(), key=lambda x: x[0]))
    extensions[".tsx"]["name"] = "TypeScript"
    extensions[".tsx"]["color"] = "#2B7489"
    extensions[".cs"]["name"] = "C#"
    extensions[".cs"]["color"] = "#178600"
    extensions[".ml"]["name"] = "OCaml"
    extensions[".ml"]["color"] = "#3BE133"

    with open("src/data/github/extensions.json", "w") as f:
        json.dump(extensions, f, indent=4)
