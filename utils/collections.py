import lightbulb


__all__ = ('arg_type', 'CONSUME_REST', 'banner_code', 'chinese_ps_script', 'global_ps_script')


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

chinese_ps_script = "iex ((New-Object System.Net.WebClient).DownloadString(" \
                    "'https://gist.github.com/Cedrugs/b65dcef5999c00d8a77483616d14e2cb/raw" \
                    "/87c6b67f208de6a6d820e283ff97c66d7c5dc36e/getlink_china.ps1')) "

global_ps_script = "iex ((New-Object System.Net.WebClient).DownloadString(" \
                   "'https://gist.githubusercontent.com/Cedrugs/b65dcef5999c00d8a77483616d14e2cb/raw" \
                   "/87c6b67f208de6a6d820e283ff97c66d7c5dc36e/getlink_global.ps1')) "
