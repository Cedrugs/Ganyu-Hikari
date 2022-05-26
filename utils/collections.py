import lightbulb


__all__ = ('arg_type', 'CONSUME_REST', 'banner_code')


CONSUME_REST = lightbulb.OptionModifier.CONSUME_REST


arg_type = {
    "<class 'int'>": 'number',
    "<class 'str'>": 'text'
}

banner_code = {
    'standard': 200,
    'event': 301,
    'weapon': 302
}
