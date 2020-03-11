# vault-aws-login
Stay authenticated in awscli with vault
without affecting other profiles that you wish to keep un-managed.

## Installation & Running

- Make sure [consul-template](https://github.com/hashicorp/consul-template) is installed and in your `$PATH`
- Run `pip3 install --upgrade vault-aws-login`
- Run `wget -O - https://nhtzr.github.io/vault-aws-login/vault-aws-config.tgz | tar -C "$HOME" -zxf -`
- Update `~/.vault-aws/config` with:
    ```
    [default]
    vault_addr = https://vault.engineering.armory.io
    #      (overrides your current VAULT_ADDR env var.)
    #      (leave it empty if you dont want such thing to happen)
    vault_login_method = <your auth type to vault>
    #      Type of authentication to use such as "userpass" or "ldap". Note this
    #      corresponds to the TYPE, not the enabled path. Use -path to specify the
    #      path where the authentication is enabled. The default is token.
    #      (leave it empty if you dont want this parameter)
    #      (use extra_vl_flags = ["-path", "/your/path"] fort the given example above)
    vault_login_username = <your vault username>
    #      The -method flag allows using other auth methods, such as userpass, github, or
    #      cert. For these, additional "K=V" pairs may be required. For example, to
    #      authenticate to the userpass auth method:
    #      $ vault login -method=userpass username=my-username
    #      (vault_login_<K> = <V> is also valid for K=V pairs other than username)
    ```

Assuming you have aws credentials under the vault secret `/aws/dev/sts/admin` and you
want to have them available to you under the aws-profile `dev`, run this command:

```
vault-aws-login -l dev &
```

This will keep consul-template running in the background keeping your `dev` aws-profile credentials
updated and valid. `aws --profile dev sts get-caller-identity` can help you double-check this.

## Overrides, Template, and Configs

As you can see, the `-l`/`--login` flag (login_id) conflates both the resulting aws-profile name and
the source vault secret which is a convenient convention, but it is not always ideal.
You can override both the aws-profile and vault secret that will correspond to a given login_id by
adding a `login_override` section in your `~/.vault-aws-login/confg` file:

```
[login_override prod]
aws_profile_name = prod
vault_secret_path = /aws/prod/sts/developer-role
```

Likewise, the `login_template` describe the generic values that correspond to each login_id:

```
[login_template]
aws_profile_name = %(login_id)s
vault_secret_path = /aws/%(login_id)s/sts/admin
```

Both the template and overrides are implemented by python3's [ConfigParser.BasicInterpolation](https://docs.python.org/3/library/configparser.html#configparser.BasicInterpolation) and [ConfigParser.get(vars=overrides)](https://docs.python.org/3/library/configparser.html#configparser.ConfigParser.get)

The above means both that
* A property in `login_template` can depend on a property in `login_override`, and viceversa.
* In case of a name clash, the property in `login_override` has higher priority

This allows the templates to render on arbitrary data, and not just the corresponding login_id
(Note: `login_id` is populated by the script itself, so it cannot be overridden)

The `[default]` config profile section contains the properties that the main script will use.
Most importantly the args given `vault login`, and the `-l`/`--login`/login_ids you want by default.
You can choose to take those properties from any other section by using the `-p`/`--profile` flag,
and you can use a completely different config file with the `-c`/`--config` flag as well.

For consul-template specific configs, you can modify `~/.vault-aws-config/credentials.hcl`
if you want to fine-tune its behavior. There's also the `~/.vault-aws-config/config` option named
`extra_ct_flags` in the config profile section (.i.e `[default]`) in case you want to add extra flags like `-once`.
If you want to keep multiple `credentials.hcl` files, you might want to setup `consul_template_hcl`
to different values in different config profile sections

# Code overview

The general workflow of this script is:
0. Log into vault if `vault token lookup` fails.
1. Generate the following json and invoke consult-template:
    ```
    [{ 'aws_profile_name': 'dev'
       'vault_secret_path': '/aws/sts/admin' }, .. ]
    ```
2. consul-template generates the following credentials file and invokes aws_credentials_merge:
    ```
    [dev]
    aws_access_key_id = <info from vault>
    aws_secret_access_key = <info from vault>
    aws_session_token = <info from vault>
    ```
3. aws_credentials_merge takes this new credentials and merges them into `~/.aws/credentials`.
