## [Unreleased]

## 0.1.0
- Improve auth performance for multiple realms by detecting the correct OIDC adapter using the requester host (old method just tried them all) Requires updated KEYCLOAK_MULTI_OIDC_JSON (see README.md).
- Better exception handling
- Less log noise
- Prospector static analysis + code cleanups
- Remove legacy keycloak_openid export from keycloak.py. It should not be used.