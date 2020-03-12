import os
import subprocess


def vault_login_if_required(
        extra_vl_flags,
        vault_addr,
        vault_login_kwargs):
    if vault_addr:
        os.environ['VAULT_ADDR'] = vault_addr
    if not is_vault_logged_in():
        vault_login(extra_vl_flags=extra_vl_flags, **vault_login_kwargs)


def is_vault_logged_in():
    return_code = subprocess.call(
        ['vault', 'token', 'lookup'],
        stdout=subprocess.DEVNULL
    )
    return return_code == 0


def vault_login(method=None, extra_vl_flags=(), **kwargs):
    subprocess.check_call([
        'vault', 'login',
        *(f'-method={value}'
          for value in (method,) if value),
        *extra_vl_flags,
        *(f'{key}={value}'
          for key, value in kwargs.items())
    ])
