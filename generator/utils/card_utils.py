def prepare_slots_for_json(slots):
    prepared_slots = []
    for slot in slots:
        prepared_slot = {
            'image': slot[0].id,
            'size': slot[1],
            'x_position': slot[2],
            'y_position': slot[3]
        }
        prepared_slots.append(prepared_slot)
    return prepared_slots
