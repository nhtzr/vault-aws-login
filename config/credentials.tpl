{{ range $login_data := env "VAULTAWS_LOGINDATA_JSON" | parseJSON -}}
{{ with secret $login_data.vault_secret_path -}}
[{{ $login_data.aws_profile_name }}]
aws_access_key_id = {{ .Data.access_key }}
aws_secret_access_key = {{ .Data.secret_key }}
aws_session_token = {{ .Data.security_token }}
{{end -}}
{{end -}}
