# Subscription Service

## Entities

- Plan
  - name
  - price
- UserAccount
  - iam_user_id (external provider)
  - name
  - email
  - billing_address
- Subscription
  - user_id
  - plan_id
  - start_date
  - end_date
  - status (active, inactive)
  - is_trial

### ERD

```mermaid
erDiagram
    Plan {
        string name
        MonetaryValue price
    }
    UserAccount {
        UUID iam_user_id
        string name
        string email
        Address billing_address
    }
    Subscription {
        UUID user_id
        UUID plan_id
        datetime start_date
        datetime end_date
        SubscriptionStatus status
        boolean is_trial
    }
    Subscription |o--|| Plan : "has"
    UserAccount ||--|| Subscription : "has"
```

## Use Cases
- Sign Up: User
- Subscribe to Plan: User
- Renew Subscription: System / User / Admin
- Cancel Subscription: User / Admin
- Create Plan: Admin

## Flowcharts

> Créditos ao @GSuaki pelos diagramas :)

### User Sign Up

```mermaid
flowchart TD
    A[Sign up] -->|input data| B(SignUp mediator)
    B -->|input data| C(IAM SignUp - Keycloak)
    B -->|input data with iam id| D(UserAccount SignUp)
```

### User Subscription

```mermaid
flowchart TD
    A[Subscribe to Plan] --> B[Charge payment]
    B --> C{Charge succeeded?}
    C --> |Yes| D[Create regular subscription]
    D --> E[Save subscription]
    C --> |No| F[Notify payment failure]
    F --> G[Create trial subscription]
    G --> E
```

### Subscription Renewal

```mermaid
flowchart TD
    A[Renew Subscription] --> B[Charge payment]
    B --> C{Charge succeeded?}
    C --> |Yes| D[Renew/extend subscription]
    D --> E[Save subscription]
    C --> |No| F[Notify payment failure]
    F --> G{Is trial?}
    G --> |Yes| H[Cancel subscription]
    G --> |No| I[Convert to trial]
    H --> E
    I --> E
```