import os


def consul_template_exec(
        login_data_json,
        consul_template_hcl, consul_template_flag, extra_ct_flags):
    os.environ['VAULTAWS_LOGINDATA_JSON'] = login_data_json
    os.execlp(
        'consul-template',
        'consul-template',
        '-config', consul_template_hcl,
        '-template', consul_template_flag,
        *extra_ct_flags
    )
