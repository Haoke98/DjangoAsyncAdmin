def get_attrs(dicts):
    attrs = ""
    for f in dicts:
        val = dicts.get(f)
        if f == 'disabled' and not val:
            continue
        if val is not None:
            if isinstance(val, bool):
                val = str(val).lower()
            attrs += '\t{}=\"{}\"'.format(f, val)
    return attrs

