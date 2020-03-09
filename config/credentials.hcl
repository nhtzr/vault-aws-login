vault {
  renew_token = false
  unwrap_token = false
  retry {
    enabled = true
    attempts = 12
    backoff = "250ms"
    max_backoff = "1m"
  }
}

