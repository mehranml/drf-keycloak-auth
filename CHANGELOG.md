## [0.4.0]
- For KeycloakMultiAuthentication, if KEYCLOAK_MULTI_OIDC_JSON is not configured fall back to KEYCLOAK_SERVER_URL if available
- Upgrade deps, Django >=4.1, DRF 3.15

## [0.3.1]
- Reduce log noise

## [0.3.0]
- Add `BackendRequestClient`  for client credential requests using Keycloak client OIDC config

## [0.2.3]
- Use the token issuer to determine the multi auth realm instead of the request host. Issuer is validated against ALLOWED_HOSTS

## [0.2.1]
- Add realm name prefix to User.username when using KEYCLOAK_MULTI_OIDC_JSON

## [0.2.0]
- Upgrade python_keycloak 3.3
- Fix exception when user has no defined roles for app
- Implement CI safety check
- Remove legacy multi OIDC without hostname

## [0.1.0]
- Improve auth performance for multiple realms by detecting the correct OIDC adapter using the requester host (old method just tried them all) Requires updated KEYCLOAK_MULTI_OIDC_JSON (see README.md).
- Better exception handling
- Less log noise
- Prospector static analysis + code cleanups
- Remove legacy keycloak_openid export from keycloak.py. It should not be used.