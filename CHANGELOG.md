## [0.3.0]
- Using KEYCLOAK_MULTI_OIDC_JSON will prefix django username with realm: and also save 'realm' field if defined
- Refactor Keycloak functions to be more portable and generic

## [0.2.0]
- Upgrade python_keycloak 3.3
- Fix exception when user has no defined roles for app
- Implement CI safety check
- Remove legacy multi OIDC without hostname

## 0.1.0
- Improve auth performance for multiple realms by detecting the correct OIDC adapter using the requester host (old method just tried them all) Requires updated KEYCLOAK_MULTI_OIDC_JSON (see README.md).
- Better exception handling
- Less log noise
- Prospector static analysis + code cleanups
- Remove legacy keycloak_openid export from keycloak.py. It should not be used.