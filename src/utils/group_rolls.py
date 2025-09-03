def group_by_color(list_rolls: list) -> dict:
    color_group = {}
    for roll in list_rolls:
        color = roll["color"]
        mts = float(roll["mts"]) if roll["mts"] else 0
        kg = float(roll["kg"]) if roll["kg"] else 0
        item = roll["item"] if roll["item"] else ""
        container = roll["container"]
        siigo_code = roll["siigo_code"]
        
        if item not in color_group:
            color_group[item] = {}


        if color in color_group[item]:
            color_group[item][color]["kg"] += kg
            color_group[item][color]["mts"] += mts
            color_group[item][color]["count_rolls"] += 1


        else:
            color_group[item][color] = {
                "mts": mts,
                "kg": kg,
                "count_rolls": 1,
                "container": container,
                "siigo_code" : siigo_code
            }

    return color_group