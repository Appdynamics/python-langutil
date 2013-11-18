from os.path import join as path_join
import sys


_cntrl_chars = map(chr, range(0x0, 0x1f) + [0x7f])


class PHPScalarException(Exception):
    pass


def _has_cntrl_chars(str):
    global cntrl_chars

    ret = False
    for char in str:
        if char in _cntrl_chars:
            ret = True
            break

    return ret


def generate_scalar(scalar_val, upper_keywords=True):
    ret = None

    if scalar_val is None:
        ret = 'null'

        if upper_keywords:
            ret = 'NULL'
    elif type(scalar_val) is bool:
        if scalar_val:
            ret = 'TRUE'
        else:
            ret = 'FALSE'

        if not upper_keywords:
            ret = ret.lower()
    elif type(scalar_val) is str:
        quote_type = '\''

        if _has_cntrl_chars(scalar_val):
            quote_type = '"'

        if quote_type in scalar_val:
            replacement = '\\%s' % (quote_type,)
            scalar_val = scalar_val.replace(quote_type, replacement)

        ret = '%s%s%s' % (quote_type, scalar_val, quote_type)
    elif type(scalar_val) is int:
        ret = '%d' % (scalar_val)
    elif type(scalar_val) is float:
        ret = '%f' % (scalar_val)

    if ret is None:
        raise PHPScalarException('Non-acceptable type: %s' %
                                 (type(scalar_val)))

    return ret


def generate_array(list_or_array, indent=2, last_level=0, end=';'):
    spaces = ''.join([' ' for i in range(0, indent)])
    end_bracket_spaces = ''.join([' ' for i in range(0, indent - last_level)])

    if type(list_or_array) in (tuple, list, set):
        parts = [
            'array(',
        ]

        for item in list_or_array:
            if type(item) not in (tuple, list, set, dict):
                parts.append('%s%s,' % (spaces, generate_scalar(item)))
            else:
                parts.append('%s%s' % (spaces,
                                       generate_array(item,
                                                      indent=indent + indent,
                                                      end=',',
                                                      last_level=indent)))

        parts.append('%s)%s' % (end_bracket_spaces, end))

        return '\n'.join(parts)

    parts = [
        'array(',
    ]

    keys = list_or_array.keys()

    if '_order' in list_or_array:
        keys = list_or_array['_order']

    for key in keys:
        value = list_or_array[key]
        is_scalar = type(value) not in (tuple, list, set, dict)
        if not is_scalar:
            value = generate_array(value, indent=indent + indent,
                                   end=',', last_level=indent)
        else:
            value = generate_scalar(value)

        key_quote_type = '\''
        current_end = ','

        if _has_cntrl_chars(key):
            key_quote_type = '"'

        if not is_scalar:
            value_quote_type = current_end = ''

        parts.append('%s%s%s%s => %s%s' % (
            spaces,
            key_quote_type, key, key_quote_type,
            value,
            current_end,
        ))

    last_line = '%s)%s' % (end_bracket_spaces, end)

    if end == ';':
        last_line = last_line[indent:]

    parts.append(last_line)

    return '\n'.join(parts)
