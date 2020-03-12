from collections import ChainMap


def gen_login_data(
        profile, config,
        login_template_section='login_template',
        login_override_section='login_override {}'):
    login_template = config[login_template_section]

    login_ids = profile['login_ids'].split(',')
    for login_id in login_ids:
        curr_vars = dict(login_id=login_id)
        curr_sect = login_override_section.format(login_id)
        override_vars = ChainMap(curr_vars, config[curr_sect]) \
            if curr_sect in config \
            else curr_vars

        aws_profile_name = login_template.get('aws_profile_name',
                                              vars=override_vars,
                                              fallback=login_id)
        vault_secret_path = login_template.get('vault_secret_path',
                                               vars=override_vars)
        yield {
            'aws_profile_name': aws_profile_name,
            'vault_secret_path': vault_secret_path}