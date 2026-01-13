# WSAI CODE Enterprise Server
> [!WARNING]
> This software is licensed under the [Polyform Free Trial License](./LICENSE). This is **NOT** an open source license. Usage is limited to 30 days per calendar year without a commercial license. If you would like to use it beyond 30 days, please [contact us](https://www.wsaicode.dev/contact).

> [!WARNING]
> This is a work in progress and may contain bugs, incomplete features, or breaking changes.

This directory contains the enterprise server used by [WSAI CODE Cloud](https://github.com/All-Hands-AI/WSAI CODE-Cloud/). The official, public version of WSAI CODE Cloud is available at
[app.wsai-code.dev](https://app.wsai-code.dev).

You may also want to check out the MIT-licensed [WSAI CODE](https://github.com/wsaicode/wsaicode)

## Extension of WSAI CODE

The code in `/enterprise` builds on top of WSAI CODE (MIT-licensed), extending its functionality. The enterprise code is entangled with WSAI CODE in two ways:

- Enterprise stacks on top of WSAI CODE. For example, the middleware in enterprise is stacked right on top of the middlewares in WSAI CODE. In `SAAS`, the middleware from BOTH repos will be present and running (which can sometimes cause conflicts)

- Enterprise overrides the implementation in WSAI CODE (only one is present at a time). For example, the server config SaasServerConfig overrides [`ServerConfig`](https://github.com/wsaicode/wsaicode/blob/main/wsaicode/server/config/server_config.py#L8) in WSAI CODE. This is done through dynamic imports ([see here](https://github.com/wsaicode/wsaicode/blob/main/wsaicode/server/config/server_config.py#L37-#L45))

Key areas that change on `SAAS` are

- Authentication
- User settings
- etc

### Authentication

| Aspect                    | WSAI CODE                                              | Enterprise                                                                                                                                 |
| ------------------------- | ------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- |
| **Authentication Method** | User adds a personal access token (PAT) through the UI | User performs OAuth through the UI. The GitHub app provides a short-lived access token and refresh token                            |
| **Token Storage**         | PAT is stored in **Settings**                          | Token is stored in **GithubTokenManager** (a file store in our backend)                                                             |
| **Authenticated status**  | We simply check if token exists in `Settings`          | We issue a signed cookie with `github_user_id` during OAuth, so subsequent requests with the cookie can be considered authenticated |

Note that in the future, authentication will happen via keycloak. All modifications for authentication will happen in enterprise.

### GitHub Service

The github service is responsible for interacting with Github APIs. As a consequence, it uses the user's token and refreshes it if need be

| Aspect                    | WSAI CODE                               | Enterprise                                            |
| ------------------------- | -------------------------------------- | ---------------------------------------------- |
| **Class used**            | `GitHubService`                        | `SaaSGitHubService`                            |
| **Token used**            | User's PAT fetched from `Settings`     | User's token fetched from `GitHubTokenManager` |
| **Refresh functionality** | **N/A**; user provides PAT for the app | Uses the `GitHubTokenManager` to refresh       |

NOTE: in the future we will simply replace the `GithubTokenManager` with keycloak. The `SaaSGithubService` should interact with keycloack instead.

# Areas that are BRITTLE!

## User ID vs User Token

- In WSAI CODE, the entire app revolves around the GitHub token the user sets. `wsaicode/server` uses `request.state.github_token` for the entire app
- On Enterprise, the entire APP resolves around the Github User ID. This is because the cookie sets it, so `wsaicode/server` AND `enterprise/server` depend on it and completly ignore `request.state.github_token` (token is fetched from `GithubTokenManager` instead)

Note that introducing GitHub User ID in WSAI CODE, for instance, will cause large breakages.
