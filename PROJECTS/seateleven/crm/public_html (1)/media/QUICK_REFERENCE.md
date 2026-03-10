# GraphQL Plugin - Quick Reference Guide

## Authentication
```http
authtoken: your-token-here
```

---

## Query Operations

### Basic Query
```graphql
query {
  <table_name> {
    <field1>
    <field2>
  }
}
```

### With Filters
```graphql
query {
  <table_name>(field_operator: value) {
    <field1>
    <field2>
  }
}
```

---

## Mutation Operations

### Create (Insert)
```graphql
mutation {
  add<TableName>(
    field1: value1,
    field2: value2
  ) {
    id
    message
  }
}
```

### Update
```graphql
mutation {
  update<TableName>(
    id: 123,
    field1: new_value
  ) {
    message
    field1
  }
}
```

### Delete
```graphql
mutation {
  delete<TableName>(id: 123) {
    message
  }
}
```

---

## Filter Operators

| Operator | Suffix | Example |
|----------|--------|---------|
| Equal | `_eq` | `status_eq: "active"` |
| Not Equal | `_ne` | `status_ne: "completed"` |
| Greater Than | `_gt` | `date_gt: "2025-12-01"` |
| Greater/Equal | `_gte` | `date_gte: "2025-12-01"` |
| Less Than | `_lt` | `date_lt: "2025-12-31"` |
| Less/Equal | `_lte` | `date_lte: "2025-12-31"` |
| Like | `_like` | `name_like: "Project%"` |
| In | `_in` | `id_in: [1, 2, 3]` |

---

## Relational Filtering

```graphql
query {
  <table_name>(
    relational_filters: "{\"foreign_key\": {\"field_operator\": \"value\"}}"
  ) {
    fields
  }
}
```

**Example:**
```graphql
query {
  tbltaskstimers(
    relational_filters: "{\"task_id\": {\"startdate_eq\": \"2025-12-12\"}}"
  ) {
    id
    task_id
    start_time
  }
}
```

---

## Common Examples

### Fetch All Staff
```json
{
  "query": "query {\n  tblstaff {\n    staffid\n    firstname\n    email\n  }\n}"
}
```

### Filter Tasks by Date
```json
{
  "query": "query {\n  tbltasks(startdate_eq: \"2025-12-12\") {\n    id\n    name\n    startdate\n  }\n}"
}
```

### Date Range
```json
{
  "query": "query {\n  tbltasks(\n    startdate_gte: \"2025-12-01\",\n    startdate_lte: \"2025-12-31\"\n  ) {\n    id\n    name\n  }\n}"
}
```

### Add New Task
```json
{
  "query": "mutation {\n  addTbltasks(\n    name: \"New Task\",\n    startdate: \"2025-12-15\"\n  ) {\n    id\n    message\n  }\n}"
}
```

### Update Task
```json
{
  "query": "mutation {\n  updateTbltasks(\n    id: 123,\n    status: \"completed\"\n  ) {\n    message\n  }\n}"
}
```

### Delete Task
```json
{
  "query": "mutation {\n  deleteTbltasks(id: 123) {\n    message\n  }\n}"
}
```

---

## cURL Example

```bash
curl -X POST https://your-domain.com/graphql \
  -H "Content-Type: application/json" \
  -H "authtoken: your-token" \
  -d '{"query": "query {\n  tblstaff {\n    staffid\n    firstname\n  }\n}"}'
```

---

## Error Responses

### Unauthorized
```json
{
  "error": {
    "message": "Unauthorized access"
  }
}
```

### Module Inactive
```json
{
  "error": {
    "message": "GraphQL Module is not active"
  }
}
```

### No Query
```json
{
  "error": {
    "message": "No query provided."
  }
}
```

---

## Tips

✅ **DO:**
- Request only needed fields
- Use server-side filtering
- Combine multiple filters
- Escape JSON properly in relational filters

❌ **DON'T:**
- Fetch all fields if you don't need them
- Filter data client-side
- Forget to escape quotes in JSON strings

---

## Limitations

- ❌ No pagination
- ❌ No sorting
- ❌ No aggregation (COUNT, SUM, etc.)
- ❌ No OR logic (only AND)
- ❌ No NULL checks
- ❌ Only one level of relational filtering

---

**For detailed documentation, see:** `OPERATIONS_DOCUMENTATION.md`
