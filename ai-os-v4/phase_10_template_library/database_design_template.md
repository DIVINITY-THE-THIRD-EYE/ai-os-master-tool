# Database Design & Schema Specification: {{DATABASE_NAME}}

> **Document Type**: Database Architecture & Schema Specification  
> **Status**: {{DOCUMENT_STATUS}}  
> **Database Engine**: {{DB_ENGINE}} (e.g., PostgreSQL 16 / MySQL 8 / MongoDB 7)  
> **Owner**: {{DBA_LEAD}}  
> **Author(s)**: {{DOCUMENT_AUTHOR}}  
> **Last Updated**: {{LAST_UPDATED}}  
> **Version**: {{DOCUMENT_VERSION}}  

---

## 1. Document Control & Revision History

| Version | Date | Author | Summary of Changes |
| :--- | :--- | :--- | :--- |
| 1.0.0 | {{LAST_UPDATED}} | {{DOCUMENT_AUTHOR}} | Initial Database Design Specification |

---

## 2. Executive Summary & Naming Conventions

### 2.1 Overview
*Instruction: Detail the target data store for {{DATABASE_NAME}}, high-level data modeling goals, expected growth, and transactional characteristics (OLTP vs OLAP).*

### 2.2 Schema Naming Standards
- **Tables**: `snake_case` plural (e.g., `users`, `order_items`)
- **Columns**: `snake_case` singular (e.g., `created_at`, `user_id`)
- **Primary Keys**: `id` (UUIDv4 or auto-incrementing BigInt)
- **Foreign Keys**: `<singular_table_name>_id` (e.g., `account_id`)
- **Indexes**: `idx_<table_name>_<column_names>`

---

## 3. Entity Relationship Diagram (ERD)

```
[ users ] 1 --- * [ orders ] 1 --- * [ order_items ]
    |
    | 1
    |
    *
[ user_profiles ]
```

---

## 4. Entity Specifications & Table Definitions

### 4.1 Table: `{{TABLE_1_NAME}}`
- **Description**: Stores primary record details for {{ENTITY_DESCRIPTION}}.
- **Estimated Rows / Month**: {{ESTIMATED_ROW_COUNT}}

| Column Name | Data Type | Constraints | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `id` | UUID | PRIMARY KEY | `gen_random_uuid()` | Unique entity ID |
| `name` | VARCHAR(255) | NOT NULL | None | Name of the record |
| `status` | VARCHAR(50) | NOT NULL | `'ACTIVE'` | Record status |
| `created_at` | TIMESTAMPTZ | NOT NULL | `CURRENT_TIMESTAMP` | Record creation timestamp |
| `updated_at` | TIMESTAMPTZ | NOT NULL | `CURRENT_TIMESTAMP` | Record last update timestamp |

#### Indexes
| Index Name | Index Type | Target Columns | Purpose |
| :--- | :--- | :--- | :--- |
| `idx_{{TABLE_1_NAME}}_status` | B-Tree | `status` | Filter queries by status |
| `idx_{{TABLE_1_NAME}}_created` | B-Tree | `created_at DESC` | Date range pagination |

---

### 4.2 Table: `{{TABLE_2_NAME}}`
- **Description**: Sub-entity or transaction log table.

| Column Name | Data Type | Constraints | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `id` | BIGINT | PRIMARY KEY | Auto-Increment | Surrogate key |
| `{{TABLE_1_NAME}}_id` | UUID | FOREIGN KEY | None | Refers to `{{TABLE_1_NAME}}.id` |
| `payload` | JSONB | NOT NULL | `'{}'` | Flexible payload attributes |

---

## 5. Migration & DDL Scripts

```sql
-- DDL for {{TABLE_1_NAME}}
CREATE TABLE IF NOT EXISTS {{TABLE_1_NAME}} (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_{{TABLE_1_NAME}}_status ON {{TABLE_1_NAME}}(status);
```

---

## 6. Data Lifecycle, Archival & Backup Strategy

- **Retention Period**: {{DATA_RETENTION_PERIOD}}
- **Archival Mechanism**: Cold storage export to S3 bucket after {{ARCHIVE_DAYS}} days
- **Backup Frequency**: Daily automated snapshots, WAL archiving for Point-In-Time Recovery (PITR)
- **RPO / RTO**: RPO <= 5 minutes, RTO <= 1 hour
