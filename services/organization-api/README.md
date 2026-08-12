# Organization API

APEX sovereign organization boundary service.

## Security invariant
Country scope is mandatory for all protected domain resources. Cross-country access is denied by default. Organization scope is enforced after country scope. Cross-border exchange must use an explicit gateway contract and must never bypass the sovereignty policy.

## Core hierarchy

Country -> Organization -> Organization Membership

## Completion contract

Every future domain service must carry `country_id` and, where applicable, `organization_id`, propagate the authenticated actor scope, enforce the sovereignty policy before resource access, and emit an audit event for denied privileged access.
