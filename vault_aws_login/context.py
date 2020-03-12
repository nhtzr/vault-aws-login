from configparser import ConfigParser, SectionProxy
from pathlib import Path


def gen_config(cli_profile_section, cli_config, cli_login,
               login_template_section='login_template'):
    config = ConfigParser(dict(
        credentials_file=Path('~/.aws/credentials').expanduser().absolute(),
        consul_template_hcl=Path('~/.vault-aws/credentials.hcl').expanduser().absolute(),
        template_source=Path('~/.vault-aws/credentials.tpl').expanduser().absolute(),
        template_dest=Path('~/.aws/vaultprovided-credentials').expanduser().absolute(),
        template_cmd='%(aws_credentials_merge_path)s '
                     '-o %(credentials_file)s '
                     '-i %(credentials_file)s %(template_dest)s',
        aws_credentials_merge_path='aws_credentials_merge',
    ))
    config.read(cli_config)

    if login_template_section not in config:
        config.add_section(login_template_section)
    if cli_profile_section not in config:
        config.add_section(cli_profile_section)
    if cli_login:
        config.set(cli_profile_section, 'login_ids', value=cli_login)

    return config


def gen_vault_login_kwargs(profile, key_prefix='vault_login_'):
    offset = len(key_prefix)  # offset for trimming key prefix
    return {
        key[offset:]: value
        for key, value
        in profile.items()
        if key.startswith(key_prefix)}


def gen_consul_template_flag(profile: SectionProxy):
    template_flag = ':'.join(filter(None, (
        profile['template_source'],
        profile['template_dest'],
        profile.get('template_cmd', fallback=None))))
    return template_flag
