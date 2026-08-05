# Logical Data Model Specification: {{DOMAIN_NAME}}

> **Document Type**: Logical & Conceptual Data Model Specification  
> **Status**: {{DOCUMENT_STATUS}}  
> **Data Architect**: {{DATA_ARCHITECT}}  
> **Domain**: {{DOMAIN_NAME}}  
> **Last Updated**: {{LAST_UPDATED}}  
> **Version**: {{DOCUMENT_VERSION}}  

---

## 1. Domain Overview & High-Level Entities

*Instruction: Describe the conceptual data domain, core entity boundaries, domain events, and state machine lifecycle for {{DOMAIN_NAME}}.*

- **Core Bounded Context**: {{BOUNDED_CONTEXT_NAME}}
- **Primary Domain Entities**: `{{ENTITY_1}}`, `{{ENTITY_2}}`, `{{ENTITY_3}}`

---

## 2. Entity Attribute Definitions

### 2.1 Entity: `{{ENTITY_1}}` (e.g., Account)
- **Conceptual Role**: Represents an active customer account subscription within the platform.

| Attribute | Data Type | Nullable? | Unique? | Business Constraints | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `accountId` | UUID | No | Yes | Immutable | Primary Identifier |
| `accountName` | String | No | No | Max length 100 | Legal entity name |
| `billingStatus` | Enum | No | No | `['ACTIVE', 'PAST_DUE', 'SUSPENDED']` | Current payment status |

---

### 2.2 Entity: `{{ENTITY_2}}` (e.g., Order)

| Attribute | Data Type | Nullable? | Unique? | Business Constraints | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `orderId` | UUID | No | Yes | Immutable | Order tracking ID |
| `accountId` | UUID | No | No | Foreign Ref to Account | Owning account |
| `totalAmount` | Decimal | No | No | Must be >= 0.00 | Monetary total |

---

## 3. Entity Relationships & Cardinality

```
+----------------+          1 : N          +----------------+
|    Account     | <---------------------> |     Order      |
+----------------+                         +----------------+
        |                                          |
        | 1 : 1                                    | 1 : N
        v                                          v
+----------------+                         +----------------+
| AccountSettings|                         |   OrderItem    |
+----------------+                         +----------------+
```

| Parent Entity | Child Entity | Relationship Type | Cardinality | Foreign Key Constraint | Delete Cascade Rule |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Account | Order | One-to-Many | `1 : 0..*` | `orders.account_id -> account.id` | RESTRICT |
| Order | OrderItem | One-to-Many | `1 : 1..*` | `order_items.order_id -> order.id` | CASCADE |

---

## 4. State Machine & Event Lifecycle

```
[ PENDING ] ---> (Payment Authorized) ---> [ PROCESSING ] ---> (Shipped) ---> [ FULFILLED ]
     |                                          |
     +-----> (Payment Declined / Cancelled) ----+---> [ CANCELLED ]
```
