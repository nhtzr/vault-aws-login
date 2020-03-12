from vault_aws_login.consul_template import consul_template_exec
from vault_aws_login.vault import vault_login_if_required
from vault_aws_login.context import gen_login_data, gen_config, gen_vault_login_kwargs, \
    gen_consul_template_flag
