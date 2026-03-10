# GraphQL Plugin - Complete Operations List

## Overview
This document provides a complete list of all operations supported by the GraphQL plugin for Perfex CRM.

---

## 1. QUERY OPERATIONS

### 1.1 Basic Query Operations

| Operation | Description | Syntax | Dynamic |
|-----------|-------------|--------|---------|
| **Fetch All Records** | Retrieve all records from any table | `<table> { fields }` | ✅ Works on all tables |
| **Fetch Specific Fields** | Select only required fields | `<table> { field1 field2 }` | ✅ All table fields |
| **Multi-Table Query** | Query multiple tables in one request | `{ table1 {...} table2 {...} }` | ✅ Any combination |

### 1.2 Filtered Query Operations

| Filter Type | Operator | Suffix | Example | Applies To |
|-------------|----------|--------|---------|------------|
| **Equal** | `=` | `_eq` | `field_eq: "value"` | All fields |
| **Not Equal** | `!=` | `_ne` | `field_ne: "value"` | All fields |
| **Greater Than** | `>` | `_gt` | `field_gt: "value"` | All fields |
| **Greater Than or Equal** | `>=` | `_gte` | `field_gte: "value"` | All fields |
| **Less Than** | `<` | `_lt` | `field_lt: "value"` | All fields |
| **Less Than or Equal** | `<=` | `_lte` | `field_lte: "value"` | All fields |
| **Pattern Match** | `LIKE` | `_like` | `field_like: "pattern%"` | All fields |
| **In List** | `IN` | `_in` | `field_in: [val1, val2]` | All fields |

**Total Filter Operators:** 8  
**Fields Supporting Filters:** All fields in all tables  
**Filter Logic:** AND (all filters must match)

### 1.3 Relational Query Operations

| Operation | Description | Syntax | Capability |
|-----------|-------------|--------|------------|
| **Foreign Key Filter** | Filter by related table conditions | `relational_filters: "json"` | ✅ All foreign keys |
| **Multi-Relation Filter** | Filter by multiple foreign keys | Multiple keys in JSON | ✅ Supported |
| **Nested Filters** | Apply all 8 operators to related tables | Standard operators in JSON | ✅ Supported |

**Supported Foreign Key Patterns:**
- `*_id` (e.g., `task_id`, `staff_id`, `project_id`)
- `id*` (e.g., `idtask`, `idstaff`)

**Related Table Mapping:**
- `task_id` → `tbltasks` or `tbltask`
- `staff_id` → `tblstaffs` or `tblstaff`
- Pattern: `tbl<name>s` or `tbl<name>`

---

## 2. MUTATION OPERATIONS

### 2.1 Create Operations (INSERT)

| Operation | Naming Pattern | Required Args | Returns | Dynamic |
|-----------|----------------|---------------|---------|---------|
| **Insert Record** | `add<TableName>` | Table-specific fields | `id`, `message`, fields | ✅ All tables |

**Example Mutations Generated:**
- `addTblstaff` - Insert staff member
- `addTbltasks` - Insert task
- `addTblprojects` - Insert project
- `add<AnyTable>` - Insert into any table

**Return Fields:**
- `id` (integer) - Auto-generated ID of inserted record
- `message` (string) - Success/failure message
- All requested table fields

### 2.2 Update Operations (UPDATE)

| Operation | Naming Pattern | Required Args | Optional Args | Returns | Dynamic |
|-----------|----------------|---------------|---------------|---------|---------|
| **Update Record** | `update<TableName>` | `id` (integer) | Any table fields | `message`, updated fields | ✅ All tables |

**Example Mutations Generated:**
- `updateTblstaff` - Update staff member
- `updateTbltasks` - Update task
- `updateTblprojects` - Update project
- `update<AnyTable>` - Update any table record

**Return Fields:**
- `message` (string) - Success/failure message
- All requested table fields with updated values

### 2.3 Delete Operations (DELETE)

| Operation | Naming Pattern | Required Args | Returns | Dynamic |
|-----------|----------------|---------------|---------|---------|
| **Delete Record** | `delete<TableName>` | `id` (integer) | `message` | ✅ All tables |

**Example Mutations Generated:**
- `deleteTblstaff` - Delete staff member
- `deleteTbltasks` - Delete task
- `deleteTblprojects` - Delete project
- `delete<AnyTable>` - Delete from any table

**Return Fields:**
- `message` (string) - Success/failure message

---

## 3. AUTHENTICATION OPERATIONS

| Operation | Method | Location | Required | Format |
|-----------|--------|----------|----------|--------|
| **Token Authentication** | Header | `authtoken` | ✅ Yes | String |

**Token Management:**
- Generated in: Admin Panel → GraphQL → Token Management
- Stored in: Database option `graphqltoken`
- Validated: On every request
- Failure Response: `403 Forbidden`

---

## 4. SCHEMA OPERATIONS

### 4.1 Dynamic Schema Generation

| Feature | Description | Automatic |
|---------|-------------|-----------|
| **Table Detection** | Scans all database tables | ✅ Yes |
| **Field Detection** | Detects all columns per table | ✅ Yes |
| **Type Inference** | Assigns GraphQL types based on field names | ✅ Yes |
| **Query Type Creation** | Creates query for each table | ✅ Yes |
| **Mutation Type Creation** | Creates add/update/delete for each table | ✅ Yes |
| **Filter Args Generation** | Creates 8 operators for each field | ✅ Yes |

### 4.2 Type Mapping

| Database Pattern | GraphQL Type | Detection Rule |
|------------------|--------------|----------------|
| `id` field | `Type::int()` | Field name equals "id" |
| `*_id` field | `Type::int()` | Field name ends with "_id" |
| `id*` field | `Type::int()` | Field name starts with "id" |
| All other fields | `Type::string()` | Default type |
| Query results | `Type::listOf()` | Array of objects |
| Required mutation args | `Type::nonNull()` | e.g., `id` in update/delete |

---

## 5. SUPPORTED OPERATIONS BY CATEGORY

### 5.1 Data Retrieval (Queries)

✅ **Supported:**
- Fetch all records from any table
- Fetch specific fields
- Query multiple tables simultaneously
- Filter by exact match
- Filter by inequality
- Filter by comparison (>, >=, <, <=)
- Filter by pattern (LIKE)
- Filter by list (IN)
- Combine multiple filters (AND logic)
- Filter by related table data (foreign keys)
- Multi-level foreign key filtering

❌ **Not Supported:**
- Pagination (LIMIT/OFFSET)
- Sorting (ORDER BY)
- Aggregation (COUNT, SUM, AVG, MIN, MAX)
- OR logic between filters
- NULL/NOT NULL checks
- Nested relations (beyond one level)
- Computed/virtual fields
- Joins (handled via relational filters)

### 5.2 Data Modification (Mutations)

✅ **Supported:**
- Insert single record
- Update single record by ID
- Delete single record by ID
- Return inserted ID
- Return updated fields
- Success/failure messages

❌ **Not Supported:**
- Batch insert
- Batch update
- Batch delete
- Conditional delete (without ID)
- Upsert operations
- Transactions
- Cascading operations

### 5.3 Advanced Features

✅ **Supported:**
- Token-based authentication
- Dynamic schema generation
- Automatic type detection
- Foreign key relationship mapping
- Multi-table queries
- Complex filter combinations
- CSRF exclusion for GraphQL endpoint

❌ **Not Supported:**
- GraphQL subscriptions
- Custom resolvers
- Field-level permissions
- Rate limiting
- Query complexity analysis
- Persisted queries
- File uploads
- Batch queries

---

## 6. OPERATION COUNTS

### Total Operations Available

| Category | Count | Details |
|----------|-------|---------|
| **Query Operations** | N × 1 | One query per table (N = number of tables) |
| **Create Mutations** | N × 1 | One `add` mutation per table |
| **Update Mutations** | N × 1 | One `update` mutation per table |
| **Delete Mutations** | N × 1 | One `delete` mutation per table |
| **Filter Operators** | 8 | Applied to all fields |
| **Total Filters** | N × F × 8 | N tables × F fields × 8 operators |

**Example:** For a database with 50 tables averaging 10 fields each:
- **50 query operations**
- **50 create mutations**
- **50 update mutations**
- **50 delete mutations**
- **4,000 filter arguments** (50 × 10 × 8)
- **Total: 200 primary operations + 4,000 filter combinations**

---

## 7. OPERATION NAMING CONVENTIONS

### 7.1 Query Naming

| Pattern | Example | Description |
|---------|---------|-------------|
| `<tablename>` | `tblstaff` | Exact table name (lowercase) |
| `<tablename>` | `tbltasks` | Exact table name (lowercase) |

**Rules:**
- Use exact database table name
- Case-sensitive
- No transformation applied

### 7.2 Mutation Naming

| Operation | Pattern | Example | Case |
|-----------|---------|---------|------|
| **Create** | `add<TableName>` | `addTblstaff` | PascalCase table name |
| **Update** | `update<TableName>` | `updateTblstaff` | PascalCase table name |
| **Delete** | `delete<TableName>` | `deleteTblstaff` | PascalCase table name |

**Rules:**
- Prefix: `add`, `update`, or `delete`
- Table name: First letter uppercase, rest as-is
- Example: `tbltasks` → `addTbltasks`, `updateTbltasks`, `deleteTbltasks`

### 7.3 Filter Naming

| Pattern | Example | Description |
|---------|---------|-------------|
| `<field>_<operator>` | `startdate_eq` | Field name + underscore + operator |
| `<field>_<operator>` | `status_ne` | Field name + underscore + operator |

**Rules:**
- Field name: Exact database column name
- Separator: Single underscore `_`
- Operator: Two or three letter code (eq, ne, gt, gte, lt, lte, like, in)

---

## 8. OPERATION CAPABILITIES MATRIX

| Feature | Query | Create | Update | Delete | Filter | Relational |
|---------|-------|--------|--------|--------|--------|------------|
| **All Tables** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **All Fields** | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
| **Type Safety** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Validation** | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Error Handling** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Batch Operations** | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Transactions** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

---

## 9. OPERATION EXAMPLES BY TYPE

### 9.1 Simple Operations

```graphql
# Query all staff
query { tblstaff { staffid firstname } }

# Query all tasks
query { tbltasks { id name } }

# Add staff
mutation { addTblstaff(firstname: "John", email: "john@example.com") { id message } }

# Update task
mutation { updateTbltasks(id: 1, status: "completed") { message } }

# Delete task
mutation { deleteTbltasks(id: 1) { message } }
```

### 9.2 Filtered Operations

```graphql
# Equal filter
query { tbltasks(status_eq: "active") { id name } }

# Range filter
query { tbltasks(startdate_gte: "2025-12-01", startdate_lte: "2025-12-31") { id name } }

# Pattern filter
query { tblstaff(firstname_like: "John%") { staffid firstname } }

# IN filter
query { tbltasks(id_in: [1, 2, 3]) { id name } }
```

### 9.3 Relational Operations

```graphql
# Filter by related table field
query {
  tbltaskstimers(
    relational_filters: "{\"task_id\": {\"startdate_eq\": \"2025-12-12\"}}"
  ) {
    id
    task_id
  }
}

# Multiple relational filters
query {
  tbltaskstimers(
    relational_filters: "{\"task_id\": {\"status_eq\": \"active\"}, \"staff_id\": {\"email_like\": \"%@example.com\"}}"
  ) {
    id
  }
}
```

### 9.4 Complex Operations

```graphql
# Multi-table with filters
query {
  tblstaff(email_like: "%@example.com") {
    staffid
    firstname
    email
  }
  tbltasks(
    startdate_gte: "2025-12-01",
    status_ne: "cancelled"
  ) {
    id
    name
    startdate
  }
}

# Combined direct and relational filters
query {
  tbltaskstimers(
    staff_id_eq: 5,
    relational_filters: "{\"task_id\": {\"startdate_eq\": \"2025-12-12\"}}"
  ) {
    id
    staff_id
    task_id
  }
}
```

---

## 10. OPERATION RESPONSE FORMATS

### 10.1 Query Response

```json
{
  "data": {
    "<table_name>": [
      {
        "field1": "value1",
        "field2": "value2"
      }
    ]
  }
}
```

### 10.2 Create Response

```json
{
  "data": {
    "add<TableName>": {
      "id": 123,
      "message": "<table> added successfully.",
      "field1": "value1"
    }
  }
}
```

### 10.3 Update Response

```json
{
  "data": {
    "update<TableName>": {
      "message": "<table> with id <id> updated successfully.",
      "field1": "new_value"
    }
  }
}
```

### 10.4 Delete Response

```json
{
  "data": {
    "delete<TableName>": {
      "message": "<table> with id <id> deleted successfully."
    }
  }
}
```

### 10.5 Error Response

```json
{
  "error": {
    "message": "Error description"
  }
}
```

---

## 11. OPERATION LIMITATIONS

### 11.1 Query Limitations

| Limitation | Impact | Workaround |
|------------|--------|------------|
| No pagination | Large result sets | Filter to reduce results |
| No sorting | Unordered results | Sort client-side |
| No aggregation | Cannot count/sum | Calculate client-side |
| No OR logic | Cannot use alternative conditions | Make multiple queries |
| No NULL checks | Cannot filter NULL values | Filter client-side |

### 11.2 Mutation Limitations

| Limitation | Impact | Workaround |
|------------|--------|------------|
| Single record only | Cannot batch insert | Loop multiple mutations |
| No validation | Invalid data may be inserted | Validate client-side |
| No transactions | Cannot rollback | Handle errors manually |
| No cascading | Related records not deleted | Delete manually |
| No upsert | Cannot insert-or-update | Check existence first |

### 11.3 General Limitations

| Limitation | Impact | Workaround |
|------------|--------|------------|
| No subscriptions | Cannot listen for changes | Poll with queries |
| No file uploads | Cannot upload files | Use separate endpoint |
| No custom resolvers | Cannot add computed fields | Calculate client-side |
| No permissions | All tables accessible | Implement in application |
| No rate limiting | Potential abuse | Implement at proxy level |

---

## 12. OPERATION SECURITY

### 12.1 Authentication

| Feature | Implementation | Status |
|---------|----------------|--------|
| Token validation | Every request | ✅ Active |
| Header-based auth | `authtoken` header | ✅ Active |
| Module activation check | Before processing | ✅ Active |
| CSRF protection | Excluded for GraphQL | ✅ Active |

### 12.2 Data Protection

| Feature | Implementation | Status |
|---------|----------------|--------|
| SQL injection protection | Query Builder parameterization | ✅ Active |
| Direct access prevention | `BASEPATH` check | ✅ Active |
| Input sanitization | CodeIgniter built-in | ✅ Active |
| Output encoding | JSON encoding | ✅ Active |

### 12.3 Not Implemented

| Feature | Status | Risk Level |
|---------|--------|------------|
| Field-level permissions | ❌ | High |
| Rate limiting | ❌ | Medium |
| Query complexity limits | ❌ | Medium |
| IP whitelisting | ❌ | Low |
| Audit logging | ❌ | Low |

---

## SUMMARY

### Total Supported Operations

**Core Operations:**
- ✅ Query (Read) - All tables
- ✅ Create (Insert) - All tables
- ✅ Update - All tables
- ✅ Delete - All tables

**Filter Operations:**
- ✅ 8 comparison operators
- ✅ Applied to all fields
- ✅ Combinable with AND logic
- ✅ Relational filtering support

**Advanced Features:**
- ✅ Multi-table queries
- ✅ Dynamic schema generation
- ✅ Token authentication
- ✅ Foreign key relationship mapping

**Total Operation Types:** 4 (Query, Create, Update, Delete)  
**Total Filter Operators:** 8  
**Total Tables Supported:** All database tables (dynamic)  
**Total Fields Supported:** All table fields (dynamic)

---

**Document Version:** 1.0  
**Last Updated:** December 16, 2025  
**Plugin Version:** 1.0.1
