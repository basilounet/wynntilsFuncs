import json

with open("Wynnilla UI/compiler/define.json", "r") as f:
    defines = json.load(f)

with open("Wynnilla UI/compiler/font/template.json", "r") as f:
    font_template = json.load(f)

with open("Wynnilla UI/compiler/info-box/template.txt", "r") as f:
    info_box_template = f.read()
    info_box_template = info_box_template.replace("\n", "").replace(" ", "").replace("|"," ")

_id = 512

def id():
    global _id
    _id += 1
    return _id

def stringify(target_id):
    return chr(target_id)

for key, offset in defines["spaces"].items():
    this_id = id()
    info_box_template = info_box_template.replace(
        f"${key}$",
        f"styled_text(from_codepoint({this_id}))")
    info_box_template = info_box_template.replace(
        f"${key}@R$",
        f"from_codepoint({this_id})")
    font_template["providers"][1]["advances"][stringify(this_id)] = offset

for mapping in defines["textures"]:
    for variant in mapping["variants"]:
        ids = [[id() for _ in range(mapping["chars"][0])] for _ in range(mapping["chars"][1])]

        info_box_template = info_box_template.replace(
            f"${variant["name"]}$",
            f"styled_text(from_codepoint({ids[0][0]}))")
        info_box_template = info_box_template.replace(
            f"${variant["name"]}@R$",
            f"from_codepoint({ids[0][0]})")

        for y, idrow in enumerate(ids):
            for x, this_id in enumerate(idrow):
                print(f"${variant["name"]}@{x + y * mapping["chars"][0]}$")
                info_box_template = info_box_template.replace(
                    f"${variant["name"]}@{x + y * mapping["chars"][0]}$",
                    f"styled_text(from_codepoint({ids[y][x]}))")
                info_box_template = info_box_template.replace(
                    f"${variant["name"]}@{x + y * mapping["chars"][0]}@R$",
                    f"from_codepoint({ids[y][x]})")

        font_template["providers"].append(
            {
                "ascent": variant["ascent"],
                "chars": ["".join(stringify(this_id) for this_id in idrow) for idrow in ids],
                "file": mapping["file"],
                "height": mapping["height"],
                "type": "bitmap"
            }
        )

# content = content\
#     .replace("\n", "")\
#     .replace(" ", "")\
#     .replace("$PAN_TO_CENTER$", cvt("F015"))\
#     .replace("$PAN_TO_RIGHT$", cvt("F015"))\
#     .replace("$PAN_TO_START$", cvt("E201"))\
#     .replace("$PAN_WIDGET_LEFT_START$", cvt("F002"))\
#     .replace("$PAN_WIDGET_NEXT$", cvt("F001"))\
#     .replace("$PAN_WIDGET_RIGHT_START$", cvt("F059"))\
#     .replace("$PAN_WIDGET_CENTER_START$", cvt("E125"))\
#     .replace("$PAN_WIDGET_CENTER_LEFT$", cvt("E009"))\
#     .replace("$PAN_WIDGET_BACK$", cvt("E013"))\
#     .replace("$PAN_WIDGET_CENTER_TOP$", cvt("F003"))\
#     .replace("$PAN_WIDGET_CENTER_RIGHT$", cvt("F003"))\
#     .replace("$PAN_WIDGET_CENTER_END$", cvt("E009"))\
#     \
#     .replace("$CORRUPTED_BAR$", cvt("0010"))\
#     .replace("$HOLY_POWER_BAR$", cvt("0010"))\
#     .replace("$CENTER_FEATURE$", cvt("0011"))\
#     .replace("$WIDGET$", cvt("0012"))\
#     .replace("$WIDGET_CENTER_CENTER$", cvt("0013"))\
#     .replace("$WIDGET_CENTER_THREE$", cvt("0014"))\
#     .replace("$WIDGET_CENTER_TOP$", cvt("0015"))\

with open("Wynnilla UI/compiler/info-box/result.txt", "w+") as f:
    f.write(info_box_template)

with open("Wynnilla UI/assets/wynnilla/font/hotbar.json", "w+") as f:
    json.dump(font_template, f, indent=2)