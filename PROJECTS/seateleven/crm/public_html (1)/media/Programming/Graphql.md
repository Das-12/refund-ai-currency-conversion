# GraphQL Filtering Guide

## Table of Contents
1. [Overview](#overview)
2. [Basic Filtering](#basic-filtering)
3. [Comparison Operators](#comparison-operators)
4. [Relational Filtering](#relational-filtering)
5. [Advanced Examples](#advanced-examples)
6. [Best Practices](#best-practices)

---

## Overview

This GraphQL API now supports advanced filtering capabilities including:
- ✅ **Field-level filtering** with comparison operators
- ✅ **Relational filtering** based on foreign key relationships
- ✅ **Multiple filter combinations** (AND logic)
- ✅ **Automatic table and field detection**

---

## Basic Filtering

### Simple Query (No Filters)
Fetch all records from a table:

```json
{
  "query": "query {\n  tbltasks {\n    id\n    name\n    startdate\n  }\n}"
}
```

### Filter by Exact Match
Use the `_eq` operator to filter by exact value:

```json
{
  "query": "query {\n  tbltasks(startdate_eq: \"2025-12-12\") {\n    id\n    name\n    startdate\n  }\n}"
}
```

---

## Comparison Operators

All fields in every table support the following operators:

| Operator | Description | Example | SQL Equivalent |
|----------|-------------|---------|----------------|
| `_eq` | Equal to | `startdate_eq: "2025-12-12"` | `WHERE startdate = '2025-12-12'` |
| `_ne` | Not equal to | `status_ne: "completed"` | `WHERE status != 'completed'` |
| `_gt` | Greater than | `startdate_gt: "2025-12-01"` | `WHERE startdate > '2025-12-01'` |
| `_gte` | Greater than or equal | `startdate_gte: "2025-12-01"` | `WHERE startdate >= '2025-12-01'` |
| `_lt` | Less than | `startdate_lt: "2025-12-31"` | `WHERE startdate < '2025-12-31'` |
| `_lte` | Less than or equal | `startdate_lte: "2025-12-31"` | `WHERE startdate <= '2025-12-31'` |
| `_like` | Pattern matching | `name_like: "Project%"` | `WHERE name LIKE 'Project%'` |
| `_in` | Match any in list | `id_in: [1, 2, 3]` | `WHERE id IN (1, 2, 3)` |

### Operator Examples

#### 1. Equal (`_eq`)
```json
{
  "query": "query {\n  tblstaff(email_eq: \"john@example.com\") {\n    staffid\n    firstname\n    lastname\n    email\n  }\n}"
}
```

#### 2. Not Equal (`_ne`)
```json
{
  "query": "query {\n  tbltasks(status_ne: \"completed\") {\n    id\n    name\n    status\n  }\n}"
}
```

#### 3. Greater Than (`_gt`)
```json
{
  "query": "query {\n  tbltasks(startdate_gt: \"2025-12-01\") {\n    id\n    name\n    startdate\n  }\n}"
}
```

#### 4. Greater Than or Equal (`_gte`)
```json
{
  "query": "query {\n  tbltasks(startdate_gte: \"2025-12-01\") {\n    id\n    name\n    startdate\n  }\n}"
}
```

#### 5. Less Than (`_lt`)
```json
{
  "query": "query {\n  tbltasks(startdate_lt: \"2025-12-31\") {\n    id\n    name\n    startdate\n  }\n}"
}
```

#### 6. Less Than or Equal (`_lte`)
```json
{
  "query": "query {\n  tbltasks(startdate_lte: \"2025-12-31\") {\n    id\n    name\n    startdate\n  }\n}"
}
```

#### 7. Pattern Matching (`_like`)
```json
{
  "query": "query {\n  tblstaff(firstname_like: \"John%\") {\n    staffid\n    firstname\n    lastname\n  }\n}"
}
```

**LIKE Pattern Wildcards:**
- `%` - Matches any sequence of characters
- `John%` - Starts with "John"
- `%Smith` - Ends with "Smith"
- `%admin%` - Contains "admin"

#### 8. IN Operator (`_in`)
```json
{
  "query": "query {\n  tbltasks(id_in: [1, 2, 3, 4, 5]) {\n    id\n    name\n    startdate\n  }\n}"
}
```

---

## Multiple Filters (AND Logic)

You can combine multiple filters on the same table. All filters are applied with **AND** logic:

### Date Range Filter
```json
{
  "query": "query {\n  tbltasks(\n    startdate_gte: \"2025-12-01\",\n    startdate_lte: \"2025-12-31\"\n  ) {\n    id\n    name\n    startdate\n  }\n}"
}
```

### Complex Multi-Field Filter
```json
{
  "query": "query {\n  tbltasks(\n    startdate_gte: \"2025-12-01\",\n    name_like: \"Project%\",\n    status_ne: \"cancelled\",\n    id_in: [1, 2, 3, 4, 5]\n  ) {\n    id\n    name\n    startdate\n    status\n  }\n}"
}
```

---

## Relational Filtering

Filter records based on conditions in related tables using foreign key relationships.

### How It Works

1. The system detects foreign key fields (e.g., `task_id`, `staff_id`)
2. Automatically maps them to related tables (e.g., `task_id` → `tbltasks`)
3. Applies filters to the related table first
4. Returns only records that match the foreign key relationship

### Relational Filter Format

```json
{
  "foreign_key_field": {
    "related_field_operator": "value"
  }
}
```

**Important:** The relational_filters value must be a **JSON string** (escaped quotes).

### Example 1: Filter Task Timers by Task Start Date

Get timers only for tasks that start on a specific date:

```json
{
  "query": "query {\n  tbltaskstimers(\n    relational_filters: \"{\\\"task_id\\\": {\\\"startdate_eq\\\": \\\"2025-12-12\\\"}}\"\n  ) {\n    id\n    staff_id\n    task_id\n    start_time\n    end_time\n    note\n  }\n}"
}
```

### Example 2: Filter Task Timers by Date Range

Get timers for tasks within a date range:

```json
{
  "query": "query {\n  tbltaskstimers(\n    relational_filters: \"{\\\"task_id\\\": {\\\"startdate_gte\\\": \\\"2025-12-01\\\", \\\"startdate_lte\\\": \\\"2025-12-31\\\"}}\"\n  ) {\n    id\n    staff_id\n    task_id\n    start_time\n    end_time\n    note\n  }\n}"
}
```

### Example 3: Filter by Task Name Pattern

Get timers for tasks whose name starts with "Project":

```json
{
  "query": "query {\n  tbltaskstimers(\n    relational_filters: \"{\\\"task_id\\\": {\\\"name_like\\\": \\\"Project%\\\"}}\"\n  ) {\n    id\n    staff_id\n    task_id\n    start_time\n    end_time\n    note\n  }\n}"
}
```

### Example 4: Combining Direct and Relational Filters

Filter by both the timer's staff AND the task's start date:

```json
{
  "query": "query {\n  tbltaskstimers(\n    staff_id_eq: 5,\n    relational_filters: \"{\\\"task_id\\\": {\\\"startdate_eq\\\": \\\"2025-12-12\\\"}}\"\n  ) {\n    id\n    staff_id\n    task_id\n    start_time\n    end_time\n    note\n  }\n}"
}
```

---

## Advanced Examples

### Example 1: Complete Staff Time Tracking Query

Get all data for tasks on a specific date:

```json
{
  "query": "query {\n  tblstaff {\n    staffid\n    firstname\n    lastname\n    email\n  }\n  tblcustomfieldsvalues {\n    relid\n    fieldid\n    value\n  }\n  tbltasks(startdate_eq: \"2025-12-12\") {\n    id\n    name\n    startdate\n  }\n  tbltaskstimers(\n    relational_filters: \"{\\\"task_id\\\": {\\\"startdate_eq\\\": \\\"2025-12-12\\\"}}\"\n  ) {\n    id\n    staff_id\n    task_id\n    start_time\n    end_time\n    note\n  }\n}"
}
```

### Example 2: Monthly Report Query

Get tasks and timers for the entire month:

```json
{
  "query": "query {\n  tbltasks(\n    startdate_gte: \"2025-12-01\",\n    startdate_lte: \"2025-12-31\"\n  ) {\n    id\n    name\n    startdate\n  }\n  tbltaskstimers(\n    relational_filters: \"{\\\"task_id\\\": {\\\"startdate_gte\\\": \\\"2025-12-01\\\", \\\"startdate_lte\\\": \\\"2025-12-31\\\"}}\"\n  ) {\n    id\n    staff_id\n    task_id\n    start_time\n    end_time\n    note\n  }\n}"
}
```

### Example 3: Staff-Specific Query

Get all tasks and timers for a specific staff member:

```json
{
  "query": "query {\n  tblstaff(staffid_eq: 5) {\n    staffid\n    firstname\n    lastname\n    email\n  }\n  tbltaskstimers(staff_id_eq: 5) {\n    id\n    staff_id\n    task_id\n    start_time\n    end_time\n    note\n  }\n}"
}
```

### Example 4: Active Projects Filter

Get only active (non-completed) tasks:

```json
{
  "query": "query {\n  tbltasks(\n    status_ne: \"completed\",\n    status_ne: \"cancelled\"\n  ) {\n    id\n    name\n    status\n    startdate\n  }\n}"
}
```

---

## Best Practices

### 1. **Use Specific Filters**
Instead of fetching all data and filtering client-side, use server-side filters:

❌ **Bad:**
```json
{
  "query": "query {\n  tbltasks {\n    id\n    name\n    startdate\n  }\n}"
}
```
Then filter in your application code.

✅ **Good:**
```json
{
  "query": "query {\n  tbltasks(startdate_eq: \"2025-12-12\") {\n    id\n    name\n    startdate\n  }\n}"
}
```

### 2. **Request Only Needed Fields**
Don't fetch fields you don't need:

❌ **Bad:**
```json
{
  "query": "query {\n  tblstaff {\n    staffid\n    firstname\n    lastname\n    email\n    phone\n    address\n    city\n    state\n    zip\n  }\n}"
}
```

✅ **Good:**
```json
{
  "query": "query {\n  tblstaff {\n    staffid\n    firstname\n    email\n  }\n}"
}
```

### 3. **Use Date Ranges Wisely**
For date ranges, use `_gte` and `_lte` together:

```json
{
  "query": "query {\n  tbltasks(\n    startdate_gte: \"2025-12-01\",\n    startdate_lte: \"2025-12-31\"\n  ) {\n    id\n    name\n    startdate\n  }\n}"
}
```

### 4. **Escape JSON Properly in Relational Filters**
When using `relational_filters`, ensure proper JSON escaping:

```json
relational_filters: "{\"task_id\": {\"startdate_eq\": \"2025-12-12\"}}"
```

### 5. **Combine Filters for Precision**
Use multiple filters to get exactly what you need:

```json
{
  "query": "query {\n  tbltaskstimers(\n    staff_id_eq: 5,\n    start_time_gte: \"2025-12-12 00:00:00\",\n    start_time_lte: \"2025-12-12 23:59:59\",\n    relational_filters: \"{\\\"task_id\\\": {\\\"status_ne\\\": \\\"cancelled\\\"}}\"\n  ) {\n    id\n    staff_id\n    task_id\n    start_time\n    end_time\n  }\n}"
}
```

---

## Common Use Cases

### Use Case 1: Daily Time Report
Get all timers for today's tasks:

```json
{
  "query": "query {\n  tbltaskstimers(\n    relational_filters: \"{\\\"task_id\\\": {\\\"startdate_eq\\\": \\\"2025-12-12\\\"}}\"\n  ) {\n    id\n    staff_id\n    task_id\n    start_time\n    end_time\n    note\n  }\n}"
}
```

### Use Case 2: Employee Time Tracking
Get all timers for a specific employee:

```json
{
  "query": "query {\n  tblstaff(staffid_eq: 5) {\n    staffid\n    firstname\n    lastname\n  }\n  tbltaskstimers(staff_id_eq: 5) {\n    id\n    task_id\n    start_time\n    end_time\n    note\n  }\n}"
}
```

### Use Case 3: Project Time Analysis
Get all timers for tasks matching a project name:

```json
{
  "query": "query {\n  tbltaskstimers(\n    relational_filters: \"{\\\"task_id\\\": {\\\"name_like\\\": \\\"Project Alpha%\\\"}}\"\n  ) {\n    id\n    staff_id\n    task_id\n    start_time\n    end_time\n  }\n}"
}
```

### Use Case 4: Custom Field Filtering
Get custom field values for specific staff:

```json
{
  "query": "query {\n  tblcustomfieldsvalues(\n    fieldid_eq: 10,\n    relid_in: [1, 2, 3, 4, 5]\n  ) {\n    relid\n    fieldid\n    value\n  }\n}"
}
```

---

## Troubleshooting

### Issue 1: Empty Results
**Problem:** Query returns empty array even though data exists.

**Solution:** Check your filter values match the database format exactly:
- Dates should match format: `YYYY-MM-DD`
- IDs should be integers, not strings
- String comparisons are case-sensitive

### Issue 2: Relational Filter Not Working
**Problem:** Relational filter doesn't filter results.

**Solution:** Ensure:
1. JSON string is properly escaped
2. Foreign key field name is correct (e.g., `task_id`, not `taskid`)
3. Related table exists and follows naming convention

### Issue 3: Syntax Error
**Problem:** GraphQL syntax error.

**Solution:** 
- Ensure newlines are escaped as `\n` in the query string
- Check all quotes are properly escaped in JSON
- Validate JSON structure

---

## API Endpoint

**URL:** `https://your-domain.com/graphql`  
**Method:** `POST`  
**Headers:**
```
Content-Type: application/json
authtoken: your-auth-token-here
```

**Request Body:**
```json
{
  "query": "your GraphQL query here"
}
```

---

## Support

For issues or questions:
1. Check this documentation
2. Verify your query syntax
3. Test with simple queries first
4. Add filters incrementally

---

**Last Updated:** December 12, 2025  
**Version:** 2.0




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


# GraphQL Plugin - Operation Flow & Architecture

## Request Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT REQUEST                          │
│                                                                 │
│  POST /graphql                                                  │
│  Headers: { authtoken: "xxx", Content-Type: "application/json" }│
│  Body: { "query": "..." }                                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AUTHENTICATION LAYER                         │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ validate_token()                                         │  │
│  │ • Extract authtoken from headers                         │  │
│  │ • Retrieve stored token from database                    │  │
│  │ • Compare tokens                                         │  │
│  │ • Return 403 if invalid                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MODULE ACTIVATION CHECK                      │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ • Check if GraphQL module is active                      │  │
│  │ • Return 403 if not active                               │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SCHEMA GENERATION                            │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 1. Get all database tables                               │  │
│  │    $tables = $this->db->list_tables()                    │  │
│  │                                                           │  │
│  │ 2. For each table:                                       │  │
│  │    ┌─────────────────────────────────────────────────┐  │  │
│  │    │ • Create Query Type                              │  │  │
│  │    │   - getFieldsFromTable()                         │  │  │
│  │    │   - getFilterArgsForTable()                      │  │  │
│  │    │   - Set resolve function                         │  │  │
│  │    │                                                   │  │  │
│  │    │ • Create Mutation Types                          │  │  │
│  │    │   - add<Table> (INSERT)                          │  │  │
│  │    │   - update<Table> (UPDATE)                       │  │  │
│  │    │   - delete<Table> (DELETE)                       │  │  │
│  │    └─────────────────────────────────────────────────┘  │  │
│  │                                                           │  │
│  │ 3. Build GraphQL Schema                                  │  │
│  │    - Query Type with all table queries                  │  │
│  │    - Mutation Type with all mutations                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    QUERY PARSING                                │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ • Extract query from request body                        │  │
│  │ • Parse GraphQL query string                             │  │
│  │ • Validate syntax                                        │  │
│  │ • Return error if invalid                                │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    QUERY EXECUTION                              │
│                                                                 │
│  Is it a QUERY or MUTATION?                                    │
│                                                                 │
│  ┌──────────────────┐              ┌──────────────────────┐    │
│  │     QUERY        │              │      MUTATION        │    │
│  │                  │              │                      │    │
│  │ ┌──────────────┐ │              │ ┌──────────────────┐ │    │
│  │ │ Resolve      │ │              │ │ CREATE (INSERT)  │ │    │
│  │ │ Function     │ │              │ │ • Insert data    │ │    │
│  │ │ Called       │ │              │ │ • Return ID      │ │    │
│  │ └──────┬───────┘ │              │ └──────────────────┘ │    │
│  │        │         │              │                      │    │
│  │        ▼         │              │ ┌──────────────────┐ │    │
│  │ ┌──────────────┐ │              │ │ UPDATE           │ │    │
│  │ │ Apply        │ │              │ │ • Find by ID     │ │    │
│  │ │ Filters      │ │              │ │ • Update fields  │ │    │
│  │ │ And Fetch    │ │              │ │ • Return result  │ │    │
│  │ └──────┬───────┘ │              │ └──────────────────┘ │    │
│  │        │         │              │                      │    │
│  │        ▼         │              │ ┌──────────────────┐ │    │
│  │   See Below      │              │ │ DELETE           │ │    │
│  └──────────────────┘              │ │ • Find by ID     │ │    │
│                                    │ │ • Delete record  │ │    │
│                                    │ │ • Return message │ │    │
│                                    │ └──────────────────┘ │    │
│                                    └──────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## Query Resolution Flow

```
┌─────────────────────────────────────────────────────────────────┐
│              applyFiltersAndFetch($table, $args)                │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │ Has relational │
                    │ filters?       │
                    └───┬────────┬───┘
                        │        │
                   YES  │        │  NO
                        │        │
                        ▼        └──────────────┐
        ┌───────────────────────────┐           │
        │ RELATIONAL FILTER PROCESS │           │
        │                           │           │
        │ 1. Parse JSON filters     │           │
        │ 2. For each foreign key:  │           │
        │    ┌─────────────────────┐│           │
        │    │ • Get related table ││           │
        │    │   (getRelatedTable  ││           │
        │    │    FromForeignKey)  ││           │
        │    │                     ││           │
        │    │ • Query related     ││           │
        │    │   table with filters││           │
        │    │   (getRelatedIds)   ││           │
        │    │                     ││           │
        │    │ • Get matching IDs  ││           │
        │    │                     ││           │
        │    │ • Apply WHERE IN    ││           │
        │    │   to main query     ││           │
        │    └─────────────────────┘│           │
        └───────────┬───────────────┘           │
                    │                           │
                    └───────────┬───────────────┘
                                │
                                ▼
                ┌───────────────────────────────┐
                │   DIRECT FILTER PROCESS       │
                │                               │
                │ For each field filter:        │
                │                               │
                │ • field_eq   → WHERE =        │
                │ • field_ne   → WHERE !=       │
                │ • field_gt   → WHERE >        │
                │ • field_gte  → WHERE >=       │
                │ • field_lt   → WHERE <        │
                │ • field_lte  → WHERE <=       │
                │ • field_like → WHERE LIKE     │
                │ • field_in   → WHERE IN       │
                └───────────┬───────────────────┘
                            │
                            ▼
                ┌───────────────────────────────┐
                │   EXECUTE DATABASE QUERY      │
                │                               │
                │   $this->db->get($table)      │
                │         ->result()            │
                └───────────┬───────────────────┘
                            │
                            ▼
                ┌───────────────────────────────┐
                │   RETURN RESULTS              │
                │                               │
                │   Array of objects            │
                └───────────────────────────────┘
```

## Schema Generation Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    getFieldsFromTable($table)                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │ Get table columns          │
                │ $this->db->list_fields()   │
                └────────────┬───────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │ For each column:           │
                │                            │
                │ ┌────────────────────────┐ │
                │ │ Is field = 'id'?       │ │
                │ │   YES → Type::int()    │ │
                │ │   NO  → Type::string() │ │
                │ └────────────────────────┘ │
                │                            │
                │ ┌────────────────────────┐ │
                │ │ Create field config:   │ │
                │ │ • type                 │ │
                │ │ • resolve function     │ │
                │ └────────────────────────┘ │
                └────────────┬───────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │ Return fields array        │
                └────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                getFilterArgsForTable($table)                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │ Get table columns          │
                └────────────┬───────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │ For each column:           │
                │                            │
                │ ┌────────────────────────┐ │
                │ │ Detect field type:     │ │
                │ │ • id, *_id, id* → int  │ │
                │ │ • others → string      │ │
                │ └────────────────────────┘ │
                │                            │
                │ ┌────────────────────────┐ │
                │ │ Create 8 operators:    │ │
                │ │ • field_eq             │ │
                │ │ • field_ne             │ │
                │ │ • field_gt             │ │
                │ │ • field_gte            │ │
                │ │ • field_lt             │ │
                │ │ • field_lte            │ │
                │ │ • field_like           │ │
                │ │ • field_in (list)      │ │
                │ └────────────────────────┘ │
                └────────────┬───────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │ Add relational_filters arg │
                │ (JSON string type)         │
                └────────────┬───────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │ Return args array          │
                └────────────────────────────┘
```

## Mutation Flow Diagrams

### CREATE (INSERT) Flow

```
┌─────────────────────────────────────────────────────────────────┐
│              mutation { add<Table>(fields) { ... } }            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │ Resolve function called    │
                │ with $args (field values)  │
                └────────────┬───────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │ Execute INSERT             │
                │ $this->db->insert(         │
                │   $table, $args            │
                │ )                          │
                └────────────┬───────────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                SUCCESS            FAILURE
                    │                 │
                    ▼                 ▼
        ┌───────────────────┐   ┌──────────────────┐
        │ Get inserted ID   │   │ Return error     │
        │ $this->db->       │   │ message          │
        │   insert_id()     │   │                  │
        └─────────┬─────────┘   └──────────────────┘
                  │
                  ▼
        ┌───────────────────┐
        │ Return:           │
        │ • id              │
        │ • message         │
        │ • requested fields│
        └───────────────────┘
```

### UPDATE Flow

```
┌─────────────────────────────────────────────────────────────────┐
│         mutation { update<Table>(id, fields) { ... } }          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │ Extract ID from args       │
                │ Remove ID from data        │
                └────────────┬───────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │ Execute UPDATE             │
                │ $this->db                  │
                │   ->where('id', $id)       │
                │   ->update($table, $data)  │
                └────────────┬───────────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                SUCCESS            FAILURE
                    │                 │
                    ▼                 ▼
        ┌───────────────────┐   ┌──────────────────┐
        │ Fetch updated row │   │ Return error     │
        │ $this->db->       │   │ message          │
        │   get_where()     │   │                  │
        └─────────┬─────────┘   └──────────────────┘
                  │
                  ▼
        ┌───────────────────┐
        │ Return:           │
        │ • message         │
        │ • updated fields  │
        └───────────────────┘
```

### DELETE Flow

```
┌─────────────────────────────────────────────────────────────────┐
│              mutation { delete<Table>(id) { ... } }             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │ Extract ID from args       │
                └────────────┬───────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │ Execute DELETE             │
                │ $this->db->delete(         │
                │   $table, ['id' => $id]    │
                │ )                          │
                └────────────┬───────────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                SUCCESS            FAILURE
                    │                 │
                    ▼                 ▼
        ┌───────────────────┐   ┌──────────────────┐
        │ Return success    │   │ Return error     │
        │ message           │   │ message          │
        └───────────────────┘   └──────────────────┘
```

## Relational Filtering Flow

```
┌─────────────────────────────────────────────────────────────────┐
│   relational_filters: "{\"task_id\": {\"startdate_eq\": ...}}"  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │ Parse JSON string          │
                │ json_decode()              │
                └────────────┬───────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │ For each foreign key:      │
                │ e.g., "task_id"            │
                └────────────┬───────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────────┐
        │ getRelatedTableFromForeignKey("task_id")   │
        │                                            │
        │ 1. Remove "_id" → "task"                   │
        │ 2. Try patterns:                           │
        │    • "tbltasks"  ✓ (found)                 │
        │    • "tbltask"                             │
        │ 3. Return first match                      │
        └────────────┬───────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────────────────────────┐
        │ getRelatedIds("tbltasks", filters)         │
        │                                            │
        │ 1. Apply filters to related table:         │
        │    • startdate_eq: "2025-12-12"            │
        │                                            │
        │ 2. Execute query on "tbltasks"             │
        │                                            │
        │ 3. Extract IDs from results:               │
        │    • [1, 5, 12, 23]                        │
        └────────────┬───────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────────────────────────┐
        │ Apply to main query:                       │
        │ $this->db->where_in('task_id', [1,5,12,23])│
        └────────────────────────────────────────────┘
```

## Type Detection Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      Field Type Detection                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │ Field name     │
                    └───┬────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ name = "id"? │ │ name ends    │ │ name starts  │
│              │ │ with "_id"?  │ │ with "id"?   │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
      YES              YES              YES
       │                │                │
       └────────────────┼────────────────┘
                        │
                        ▼
                ┌──────────────┐
                │ Type::int()  │
                └──────────────┘
                        
                       NO (all)
                        │
                        ▼
                ┌──────────────┐
                │Type::string()│
                └──────────────┘
```

## Complete Request-Response Cycle

```
CLIENT                    SERVER                     DATABASE
  │                         │                            │
  │  POST /graphql          │                            │
  │  + authtoken            │                            │
  │────────────────────────>│                            │
  │                         │                            │
  │                         │ Validate Token             │
  │                         │ Check Module Active        │
  │                         │                            │
  │                         │ Get Tables                 │
  │                         │───────────────────────────>│
  │                         │<───────────────────────────│
  │                         │ [table1, table2, ...]      │
  │                         │                            │
  │                         │ For each table:            │
  │                         │   Get Fields               │
  │                         │───────────────────────────>│
  │                         │<───────────────────────────│
  │                         │ [field1, field2, ...]      │
  │                         │                            │
  │                         │ Generate Schema            │
  │                         │ Parse Query                │
  │                         │                            │
  │                         │ Execute Query/Mutation     │
  │                         │───────────────────────────>│
  │                         │<───────────────────────────│
  │                         │ Results                    │
  │                         │                            │
  │                         │ Format Response            │
  │<────────────────────────│                            │
  │  JSON Response          │                            │
  │                         │                            │
```

## Error Handling Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         REQUEST RECEIVED                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │ Token valid?   │
                    └───┬────────┬───┘
                        │        │
                       NO       YES
                        │        │
                        ▼        │
            ┌───────────────┐   │
            │ Return 403    │   │
            │ "Unauthorized"│   │
            └───────────────┘   │
                                │
                                ▼
                    ┌────────────────┐
                    │ Module active? │
                    └───┬────────┬───┘
                        │        │
                       NO       YES
                        │        │
                        ▼        │
            ┌───────────────┐   │
            │ Return 403    │   │
            │ "Not active"  │   │
            └───────────────┘   │
                                │
                                ▼
                    ┌────────────────┐
                    │ Query provided?│
                    └───┬────────┬───┘
                        │        │
                       NO       YES
                        │        │
                        ▼        │
            ┌───────────────┐   │
            │ Return error  │   │
            │ "No query"    │   │
            └───────────────┘   │
                                │
                                ▼
                    ┌────────────────┐
                    │ Execute query  │
                    └───┬────────┬───┘
                        │        │
                    ERROR      SUCCESS
                        │        │
                        ▼        ▼
            ┌───────────────┐   ┌───────────────┐
            │ Catch         │   │ Return data   │
            │ Exception     │   │ in JSON       │
            │ Return error  │   └───────────────┘
            └───────────────┘
```

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                         │
│  • HTTP Request/Response                                        │
│  • JSON Encoding/Decoding                                       │
│  • Header Processing                                            │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌─────────────────────────────────────────────────────────────────┐
│                      SECURITY LAYER                             │
│  • Token Authentication                                         │
│  • Module Activation Check                                      │
│  • CSRF Exclusion                                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌─────────────────────────────────────────────────────────────────┐
│                      GRAPHQL LAYER                              │
│  • Schema Generation                                            │
│  • Query Parsing                                                │
│  • Type System                                                  │
│  • Resolvers                                                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌─────────────────────────────────────────────────────────────────┐
│                      BUSINESS LOGIC LAYER                       │
│  • Field Detection                                              │
│  • Filter Processing                                            │
│  • Relational Mapping                                           │
│  • Query Building                                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌─────────────────────────────────────────────────────────────────┐
│                      DATA ACCESS LAYER                          │
│  • CodeIgniter Query Builder                                    │
│  • Database Connection                                          │
│  • Result Formatting                                            │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌─────────────────────────────────────────────────────────────────┐
│                      DATABASE LAYER                             │
│  • MySQL/MariaDB                                                │
│  • Tables & Columns                                             │
│  • Data Storage                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Component Interaction Map

```
┌──────────────────────────────────────────────────────────────────┐
│              GraphqlIntegrationController                        │
│                                                                  │
│  ┌────────────────┐  ┌────────────────┐  ┌─────────────────┐   │
│  │ validate_token │  │     index      │  │getFieldsFromTable│  │
│  │                │  │                │  │                 │   │
│  │ • Check auth   │  │ • Generate     │  │ • List fields   │   │
│  │ • Return 403   │  │   schema       │  │ • Detect types  │   │
│  │   if invalid   │  │ • Parse query  │  │ • Create config │   │
│  └────────┬───────┘  │ • Execute      │  └────────┬────────┘   │
│           │          │ • Return JSON  │           │            │
│           │          └────────┬───────┘           │            │
│           │                   │                   │            │
│           │          ┌────────▼───────┐           │            │
│           │          │getFilterArgs   │           │            │
│           │          │ForTable        │           │            │
│           │          │                │           │            │
│           │          │ • Create 8 ops │           │            │
│           │          │ • Add relational│          │            │
│           │          └────────┬───────┘           │            │
│           │                   │                   │            │
│           │          ┌────────▼───────────────────▼────┐       │
│           │          │ applyFiltersAndFetch           │       │
│           │          │                                │       │
│           │          │ • Process relational filters   │       │
│           │          │ • Apply direct filters         │       │
│           │          │ • Execute query                │       │
│           │          └────────┬───────────────────────┘       │
│           │                   │                               │
│           │          ┌────────▼──────────┐                    │
│           │          │getRelatedTable    │                    │
│           │          │FromForeignKey     │                    │
│           │          │                   │                    │
│           │          │ • Parse FK name   │                    │
│           │          │ • Find table      │                    │
│           │          └────────┬──────────┘                    │
│           │                   │                               │
│           │          ┌────────▼──────────┐                    │
│           │          │ getRelatedIds     │                    │
│           │          │                   │                    │
│           │          │ • Query related   │                    │
│           │          │ • Extract IDs     │                    │
│           │          └───────────────────┘                    │
│           │                                                   │
└───────────┼───────────────────────────────────────────────────┘
            │
            ▼
┌───────────────────────────────────────────────────────────────┐
│                    External Dependencies                      │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │ GraphQL-PHP  │  │ CodeIgniter  │  │ Database         │   │
│  │ Library      │  │ Framework    │  │ (MySQL/MariaDB)  │   │
│  │              │  │              │  │                  │   │
│  │ • Schema     │  │ • Query      │  │ • Tables         │   │
│  │ • Types      │  │   Builder    │  │ • Columns        │   │
│  │ • Execution  │  │ • Database   │  │ • Data           │   │
│  └──────────────┘  └──────────────┘  └──────────────────┘   │
└───────────────────────────────────────────────────────────────┘
```

---

**Document Version:** 1.0  
**Last Updated:** December 16, 2025  
**Plugin Version:** 1.0.1


# GraphQL Plugin - Complete Operations Documentation

## Table of Contents
1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Query Operations](#query-operations)
4. [Mutation Operations](#mutation-operations)
5. [Filtering Operations](#filtering-operations)
6. [Relational Operations](#relational-operations)
7. [Technical Implementation](#technical-implementation)
8. [API Reference](#api-reference)

---

## Overview

This GraphQL plugin for Perfex CRM provides a comprehensive API for querying and manipulating all database tables through GraphQL. The plugin automatically generates GraphQL schemas based on your database structure, supporting dynamic queries, mutations, and advanced filtering.

### Key Features
- ✅ **Auto-generated schemas** for all database tables
- ✅ **Full CRUD operations** (Create, Read, Update, Delete)
- ✅ **Advanced filtering** with 8 comparison operators
- ✅ **Relational filtering** based on foreign key relationships
- ✅ **Token-based authentication**
- ✅ **Dynamic field detection**
- ✅ **Type-safe operations**

### Version Information
- **Plugin Version:** 1.0.1
- **Minimum Perfex CRM Version:** 2.9.*
- **GraphQL Library:** webonyx/graphql-php

---

## Authentication

All GraphQL requests require token-based authentication.

### Authentication Method
**Header-based authentication using `authtoken`**

```http
POST /graphql
Content-Type: application/json
authtoken: your-generated-token-here
```

### Token Management
- Tokens are managed through the admin panel: `Admin → GraphQL → Token Management`
- Each request validates the token against the stored value in the database
- Invalid or missing tokens return a `403 Forbidden` response

### Authentication Response
**Unauthorized Access:**
```json
{
  "error": {
    "message": "Unauthorized access"
  }
}
```

---

## Query Operations

Query operations allow you to **read data** from any table in the database.

### 1. Basic Query (Fetch All Records)

Retrieve all records from a table without filters.

**Operation Type:** `Query`

**Syntax:**
```graphql
query {
  <table_name> {
    <field1>
    <field2>
    ...
  }
}
```

**Example: Fetch all staff members**
```json
{
  "query": "query {\n  tblstaff {\n    staffid\n    firstname\n    lastname\n    email\n  }\n}"
}
```

**Response:**
```json
{
  "data": {
    "tblstaff": [
      {
        "staffid": "1",
        "firstname": "John",
        "lastname": "Doe",
        "email": "john@example.com"
      },
      {
        "staffid": "2",
        "firstname": "Jane",
        "lastname": "Smith",
        "email": "jane@example.com"
      }
    ]
  }
}
```

### 2. Multi-Table Query

Query multiple tables in a single request.

**Example: Fetch staff and tasks**
```json
{
  "query": "query {\n  tblstaff {\n    staffid\n    firstname\n    lastname\n  }\n  tbltasks {\n    id\n    name\n    startdate\n  }\n}"
}
```

**Response:**
```json
{
  "data": {
    "tblstaff": [...],
    "tbltasks": [...]
  }
}
```

### 3. Filtered Query

Apply filters to narrow down results (see [Filtering Operations](#filtering-operations) for details).

**Example: Fetch tasks starting on a specific date**
```json
{
  "query": "query {\n  tbltasks(startdate_eq: \"2025-12-12\") {\n    id\n    name\n    startdate\n  }\n}"
}
```

### 4. Field Selection

Request only the fields you need to optimize performance.

**Example: Minimal staff data**
```json
{
  "query": "query {\n  tblstaff {\n    staffid\n    email\n  }\n}"
}
```

### Query Operation Capabilities

| Capability | Supported | Description |
|------------|-----------|-------------|
| **All Tables** | ✅ | Query any table in the database |
| **Field Selection** | ✅ | Choose specific fields to return |
| **Multi-Table** | ✅ | Query multiple tables in one request |
| **Filtering** | ✅ | Apply filters with comparison operators |
| **Relational Filtering** | ✅ | Filter based on related table data |
| **Pagination** | ❌ | Not currently supported |
| **Sorting** | ❌ | Not currently supported |
| **Aggregation** | ❌ | Not currently supported |

---

## Mutation Operations

Mutation operations allow you to **create, update, and delete** records.

### 1. Create (Insert) Operation

Add new records to any table.

**Operation Type:** `Mutation`  
**Naming Convention:** `add<TableName>`

**Syntax:**
```graphql
mutation {
  add<TableName>(
    <field1>: <value1>,
    <field2>: <value2>,
    ...
  ) {
    id
    message
    <field1>
    <field2>
    ...
  }
}
```

**Example: Add a new task**
```json
{
  "query": "mutation {\n  addTbltasks(\n    name: \"New Project Task\",\n    startdate: \"2025-12-15\",\n    status: \"in_progress\"\n  ) {\n    id\n    message\n    name\n    startdate\n  }\n}"
}
```

**Success Response:**
```json
{
  "data": {
    "addTbltasks": {
      "id": 123,
      "message": "tbltasks added successfully.",
      "name": "New Project Task",
      "startdate": "2025-12-15"
    }
  }
}
```

**Failure Response:**
```json
{
  "data": {
    "addTbltasks": {
      "message": "Failed to add tbltasks."
    }
  }
}
```

### 2. Update Operation

Modify existing records by ID.

**Operation Type:** `Mutation`  
**Naming Convention:** `update<TableName>`

**Syntax:**
```graphql
mutation {
  update<TableName>(
    id: <record_id>,
    <field1>: <new_value1>,
    <field2>: <new_value2>,
    ...
  ) {
    message
    <field1>
    <field2>
    ...
  }
}
```

**Example: Update a task**
```json
{
  "query": "mutation {\n  updateTbltasks(\n    id: 123,\n    name: \"Updated Task Name\",\n    status: \"completed\"\n  ) {\n    message\n    id\n    name\n    status\n  }\n}"
}
```

**Success Response:**
```json
{
  "data": {
    "updateTbltasks": {
      "message": "tbltasks with id 123 updated successfully.",
      "id": "123",
      "name": "Updated Task Name",
      "status": "completed"
    }
  }
}
```

**No Record Found Response:**
```json
{
  "data": {
    "updateTbltasks": {
      "message": "No rows updated. Check if the id exists."
    }
  }
}
```

### 3. Delete Operation

Remove records by ID.

**Operation Type:** `Mutation`  
**Naming Convention:** `delete<TableName>`

**Syntax:**
```graphql
mutation {
  delete<TableName>(id: <record_id>) {
    message
  }
}
```

**Example: Delete a task**
```json
{
  "query": "mutation {\n  deleteTbltasks(id: 123) {\n    message\n  }\n}"
}
```

**Success Response:**
```json
{
  "data": {
    "deleteTbltasks": {
      "message": "tbltasks with id 123 deleted successfully."
    }
  }
}
```

**No Record Found Response:**
```json
{
  "data": {
    "deleteTbltasks": {
      "message": "No rows deleted. Check if the id exists."
    }
  }
}
```

### Mutation Operation Summary

| Operation | Naming Pattern | Required Fields | Returns |
|-----------|----------------|-----------------|---------|
| **Create** | `add<TableName>` | Table-specific fields | `id`, `message`, requested fields |
| **Update** | `update<TableName>` | `id` + fields to update | `message`, updated fields |
| **Delete** | `delete<TableName>` | `id` | `message` |

---

## Filtering Operations

The plugin supports **8 comparison operators** for filtering query results.

### Supported Operators

| Operator | Description | GraphQL Suffix | SQL Equivalent | Example |
|----------|-------------|----------------|----------------|---------|
| **Equal** | Exact match | `_eq` | `WHERE field = value` | `startdate_eq: "2025-12-12"` |
| **Not Equal** | Exclude match | `_ne` | `WHERE field != value` | `status_ne: "completed"` |
| **Greater Than** | Value is greater | `_gt` | `WHERE field > value` | `startdate_gt: "2025-12-01"` |
| **Greater Than or Equal** | Value is greater or equal | `_gte` | `WHERE field >= value` | `startdate_gte: "2025-12-01"` |
| **Less Than** | Value is less | `_lt` | `WHERE field < value` | `startdate_lt: "2025-12-31"` |
| **Less Than or Equal** | Value is less or equal | `_lte` | `WHERE field <= value` | `startdate_lte: "2025-12-31"` |
| **Like** | Pattern matching | `_like` | `WHERE field LIKE value` | `name_like: "Project%"` |
| **In** | Match any in list | `_in` | `WHERE field IN (values)` | `id_in: [1, 2, 3]` |

### Filter Examples

#### 1. Equal Filter (`_eq`)
```json
{
  "query": "query {\n  tblstaff(email_eq: \"john@example.com\") {\n    staffid\n    firstname\n    email\n  }\n}"
}
```

#### 2. Not Equal Filter (`_ne`)
```json
{
  "query": "query {\n  tbltasks(status_ne: \"completed\") {\n    id\n    name\n    status\n  }\n}"
}
```

#### 3. Date Range Filter (`_gte` + `_lte`)
```json
{
  "query": "query {\n  tbltasks(\n    startdate_gte: \"2025-12-01\",\n    startdate_lte: \"2025-12-31\"\n  ) {\n    id\n    name\n    startdate\n  }\n}"
}
```

#### 4. Pattern Matching (`_like`)
```json
{
  "query": "query {\n  tblstaff(firstname_like: \"John%\") {\n    staffid\n    firstname\n    lastname\n  }\n}"
}
```

**LIKE Wildcards:**
- `%` - Matches any sequence of characters
- `John%` - Starts with "John"
- `%Smith` - Ends with "Smith"
- `%admin%` - Contains "admin"

#### 5. IN Filter (`_in`)
```json
{
  "query": "query {\n  tbltasks(id_in: [1, 2, 3, 4, 5]) {\n    id\n    name\n  }\n}"
}
```

### Multiple Filters (AND Logic)

Combine multiple filters - all are applied with **AND** logic.

**Example: Complex multi-field filter**
```json
{
  "query": "query {\n  tbltasks(\n    startdate_gte: \"2025-12-01\",\n    name_like: \"Project%\",\n    status_ne: \"cancelled\",\n    id_in: [1, 2, 3, 4, 5]\n  ) {\n    id\n    name\n    startdate\n    status\n  }\n}"
}
```

### Filter Availability

| Feature | Supported |
|---------|-----------|
| **All Fields** | ✅ All table fields support all operators |
| **Type Detection** | ✅ Automatic (ID fields = int, others = string) |
| **AND Logic** | ✅ Multiple filters combined with AND |
| **OR Logic** | ❌ Not currently supported |
| **NULL Checks** | ❌ Not currently supported |
| **Case Sensitivity** | ✅ String comparisons are case-sensitive |

---

## Relational Operations

Filter records based on conditions in **related tables** using foreign key relationships.

### How Relational Filtering Works

1. **Foreign Key Detection**: System detects fields ending with `_id` or starting with `id`
2. **Table Mapping**: Automatically maps to related tables (e.g., `task_id` → `tbltasks`)
3. **Filter Application**: Applies filters to related table first
4. **Result Filtering**: Returns only records matching the foreign key relationship

### Relational Filter Syntax

**Parameter:** `relational_filters`  
**Type:** JSON string (must be escaped)

```graphql
relational_filters: "{\"foreign_key\": {\"field_operator\": \"value\"}}"
```

### Foreign Key to Table Mapping

The system uses these patterns to find related tables:

| Foreign Key | Possible Tables | Example |
|-------------|-----------------|---------|
| `task_id` | `tbltasks`, `tbltask` | `task_id` → `tbltasks` |
| `staff_id` | `tblstaffs`, `tblstaff` | `staff_id` → `tblstaff` |
| `project_id` | `tblprojects`, `tblproject` | `project_id` → `tblprojects` |

**Pattern Rules:**
1. Remove `_id` suffix from foreign key
2. Try `tbl<name>s` (plural)
3. Try `tbl<name>` (singular)
4. Use first matching table that exists

### Relational Filter Examples

#### Example 1: Filter by Related Date
Get timers for tasks starting on a specific date:

```json
{
  "query": "query {\n  tbltaskstimers(\n    relational_filters: \"{\\\"task_id\\\": {\\\"startdate_eq\\\": \\\"2025-12-12\\\"}}\"\n  ) {\n    id\n    staff_id\n    task_id\n    start_time\n    end_time\n  }\n}"
}
```

#### Example 2: Filter by Related Date Range
Get timers for tasks within a date range:

```json
{
  "query": "query {\n  tbltaskstimers(\n    relational_filters: \"{\\\"task_id\\\": {\\\"startdate_gte\\\": \\\"2025-12-01\\\", \\\"startdate_lte\\\": \\\"2025-12-31\\\"}}\"\n  ) {\n    id\n    task_id\n    start_time\n    end_time\n  }\n}"
}
```

#### Example 3: Filter by Related Pattern
Get timers for tasks whose name starts with "Project":

```json
{
  "query": "query {\n  tbltaskstimers(\n    relational_filters: \"{\\\"task_id\\\": {\\\"name_like\\\": \\\"Project%\\\"}}\"\n  ) {\n    id\n    task_id\n    start_time\n    end_time\n  }\n}"
}
```

#### Example 4: Combine Direct and Relational Filters
Filter by both timer's staff AND task's start date:

```json
{
  "query": "query {\n  tbltaskstimers(\n    staff_id_eq: 5,\n    relational_filters: \"{\\\"task_id\\\": {\\\"startdate_eq\\\": \\\"2025-12-12\\\"}}\"\n  ) {\n    id\n    staff_id\n    task_id\n    start_time\n    end_time\n  }\n}"
}
```

#### Example 5: Multiple Related Filters
Filter by multiple foreign key relationships:

```json
{
  "query": "query {\n  tbltaskstimers(\n    relational_filters: \"{\\\"task_id\\\": {\\\"startdate_eq\\\": \\\"2025-12-12\\\"}, \\\"staff_id\\\": {\\\"email_like\\\": \\\"%@example.com\\\"}}\"\n  ) {\n    id\n    staff_id\n    task_id\n    start_time\n  }\n}"
}
```

### Relational Filtering Capabilities

| Feature | Supported | Notes |
|---------|-----------|-------|
| **Foreign Key Detection** | ✅ | Fields with `_id` suffix or `id` prefix |
| **Auto Table Mapping** | ✅ | Follows `tbl<name>s` or `tbl<name>` pattern |
| **All Filter Operators** | ✅ | Supports all 8 comparison operators |
| **Multiple Relations** | ✅ | Filter by multiple foreign keys |
| **Nested Relations** | ❌ | Only one level of relationship |
| **Custom Mappings** | ❌ | Uses convention-based mapping only |

---

## Technical Implementation

### Architecture Overview

```
GraphqlIntegrationController
├── Authentication (validate_token)
├── Schema Generation (index)
│   ├── Query Type Generation
│   │   └── Dynamic field detection per table
│   ├── Mutation Type Generation
│   │   ├── Add mutations
│   │   ├── Update mutations
│   │   └── Delete mutations
│   └── Filter Arguments Generation
├── Field Detection (getFieldsFromTable)
├── Filter Generation (getFilterArgsForTable)
├── Query Execution (applyFiltersAndFetch)
├── Relational Mapping (getRelatedTableFromForeignKey)
└── Relational Filtering (getRelatedIds)
```

### Core Components

#### 1. Schema Generation
**Location:** `GraphqlIntegrationController::index()`

- Dynamically generates GraphQL schema from database tables
- Creates query and mutation types for each table
- Automatically detects field types (int for IDs, string for others)

#### 2. Field Detection
**Location:** `GraphqlIntegrationController::getFieldsFromTable()`

- Retrieves all columns from a table
- Maps database types to GraphQL types
- Handles both object and array result formats

#### 3. Filter Arguments
**Location:** `GraphqlIntegrationController::getFilterArgsForTable()`

- Generates 8 filter operators for each field
- Detects ID fields for proper type assignment
- Adds relational filter support

#### 4. Query Execution
**Location:** `GraphqlIntegrationController::applyFiltersAndFetch()`

- Processes relational filters first
- Applies direct field filters
- Executes database query with CodeIgniter Query Builder

#### 5. Relational Mapping
**Location:** `GraphqlIntegrationController::getRelatedTableFromForeignKey()`

- Extracts table name from foreign key
- Checks multiple naming patterns
- Returns first matching table

#### 6. Relational ID Resolution
**Location:** `GraphqlIntegrationController::getRelatedIds()`

- Queries related table with filters
- Extracts IDs from results
- Returns array of matching IDs

### Type System

| Database Type | GraphQL Type | Detection Rule |
|---------------|--------------|----------------|
| **Integer** | `Type::int()` | Field name is `id` or contains `_id` or starts with `id` |
| **String** | `Type::string()` | All other fields |
| **List** | `Type::listOf()` | Used for `_in` operators and query results |
| **Non-Null** | `Type::nonNull()` | Used for required mutation arguments (e.g., `id` in update/delete) |

### Database Integration

**ORM:** CodeIgniter Query Builder  
**Connection:** Loaded via `$this->load->database()`

**Query Builder Methods Used:**
- `list_tables()` - Get all database tables
- `list_fields($table)` - Get table columns
- `table_exists($table)` - Check table existence
- `get($table)` - Fetch records
- `get_where($table, $where)` - Fetch with conditions
- `where($field, $value)` - Add WHERE clause
- `where_in($field, $values)` - Add WHERE IN clause
- `like($field, $value)` - Add LIKE clause
- `insert($table, $data)` - Insert record
- `update($table, $data)` - Update record
- `delete($table, $where)` - Delete record
- `insert_id()` - Get last inserted ID

### Security Features

1. **Token Authentication**: Every request validates `authtoken` header
2. **Module Activation Check**: Verifies GraphQL module is active
3. **CSRF Exclusion**: GraphQL endpoint excluded from CSRF protection
4. **SQL Injection Protection**: Uses Query Builder parameterized queries
5. **Direct Access Prevention**: `defined('BASEPATH')` check in all files

---

## API Reference

### Endpoint

**URL:** `https://your-domain.com/graphql`  
**Method:** `POST`  
**Content-Type:** `application/json`

### Request Headers

```http
Content-Type: application/json
authtoken: your-auth-token-here
```

### Request Body Format

```json
{
  "query": "GraphQL query string with escaped newlines"
}
```

### Response Format

**Success Response:**
```json
{
  "data": {
    "<query_or_mutation_name>": {
      // Result data
    }
  }
}
```

**Error Response:**
```json
{
  "error": {
    "message": "Error description"
  }
}
```

### HTTP Status Codes

| Code | Meaning | Scenario |
|------|---------|----------|
| **200** | Success | Query/mutation executed successfully |
| **403** | Forbidden | Invalid/missing auth token or module inactive |
| **500** | Server Error | GraphQL execution error or database error |

### Common Error Messages

| Error Message | Cause | Solution |
|---------------|-------|----------|
| `Unauthorized access` | Invalid or missing `authtoken` | Verify token in admin panel |
| `GraphQL Module is not active` | Module is deactivated | Activate module in Perfex CRM |
| `No tables found in the database` | Database connection issue | Check database configuration |
| `No query provided` | Empty or missing query field | Include `query` in request body |

### Example cURL Request

```bash
curl -X POST https://your-domain.com/graphql \
  -H "Content-Type: application/json" \
  -H "authtoken: your-token-here" \
  -d '{
    "query": "query {\n  tblstaff {\n    staffid\n    firstname\n    email\n  }\n}"
  }'
```

### Example JavaScript (Fetch API)

```javascript
const query = `
  query {
    tblstaff {
      staffid
      firstname
      email
    }
  }
`;

fetch('https://your-domain.com/graphql', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'authtoken': 'your-token-here'
  },
  body: JSON.stringify({ query })
})
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
```

### Example PHP

```php
$query = <<<'GRAPHQL'
query {
  tblstaff {
    staffid
    firstname
    email
  }
}
GRAPHQL;

$ch = curl_init('https://your-domain.com/graphql');
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'authtoken: your-token-here'
]);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode(['query' => $query]));

$response = curl_exec($ch);
curl_close($ch);

$data = json_decode($response, true);
print_r($data);
```

---

## Operation Summary Table

### Query Operations

| Operation | Syntax | Purpose | Example |
|-----------|--------|---------|---------|
| **Basic Query** | `<table> { fields }` | Fetch all records | `tblstaff { staffid firstname }` |
| **Filtered Query** | `<table>(filter) { fields }` | Fetch with conditions | `tbltasks(status_eq: "active") { id name }` |
| **Multi-Table** | Multiple table queries | Fetch from multiple tables | See examples above |
| **Relational** | `relational_filters: "json"` | Filter by related data | See relational section |

### Mutation Operations

| Operation | Naming | Required Args | Purpose |
|-----------|--------|---------------|---------|
| **Create** | `add<Table>` | Table fields | Insert new record |
| **Update** | `update<Table>` | `id` + fields | Modify existing record |
| **Delete** | `delete<Table>` | `id` | Remove record |

### Filter Operators

| Operator | Suffix | Type | Use Case |
|----------|--------|------|----------|
| Equal | `_eq` | Any | Exact match |
| Not Equal | `_ne` | Any | Exclusion |
| Greater Than | `_gt` | Comparable | Range start (exclusive) |
| Greater/Equal | `_gte` | Comparable | Range start (inclusive) |
| Less Than | `_lt` | Comparable | Range end (exclusive) |
| Less/Equal | `_lte` | Comparable | Range end (inclusive) |
| Like | `_like` | String | Pattern matching |
| In | `_in` | Array | Multiple value match |

---

## Best Practices

### 1. Request Only Needed Fields
❌ **Bad:** Fetch all fields
```json
{"query": "query { tblstaff { staffid firstname lastname email phone address city state zip country } }"}
```

✅ **Good:** Fetch only required fields
```json
{"query": "query { tblstaff { staffid firstname email } }"}
```

### 2. Use Server-Side Filtering
❌ **Bad:** Fetch all, filter client-side
```json
{"query": "query { tbltasks { id name startdate } }"}
// Then filter in application
```

✅ **Good:** Filter on server
```json
{"query": "query { tbltasks(startdate_eq: \"2025-12-12\") { id name startdate } }"}
```

### 3. Combine Filters for Precision
✅ **Good:** Use multiple filters
```json
{
  "query": "query {\n  tbltasks(\n    startdate_gte: \"2025-12-01\",\n    startdate_lte: \"2025-12-31\",\n    status_ne: \"cancelled\"\n  ) {\n    id\n    name\n  }\n}"
}
```

### 4. Proper JSON Escaping in Relational Filters
✅ **Correct escaping:**
```json
"relational_filters": "{\\\"task_id\\\": {\\\"startdate_eq\\\": \\\"2025-12-12\\\"}}"
```

### 5. Use Date Ranges with GTE/LTE
✅ **Good:** Inclusive range
```json
{
  "query": "query {\n  tbltasks(\n    startdate_gte: \"2025-12-01\",\n    startdate_lte: \"2025-12-31\"\n  ) { id name }\n}"
}
```

---

## Limitations

| Feature | Status | Notes |
|---------|--------|-------|
| **Pagination** | ❌ Not Supported | Fetch all matching records |
| **Sorting** | ❌ Not Supported | Results in database order |
| **Aggregation** | ❌ Not Supported | No COUNT, SUM, AVG, etc. |
| **OR Logic** | ❌ Not Supported | Only AND for multiple filters |
| **NULL Checks** | ❌ Not Supported | Cannot filter by NULL/NOT NULL |
| **Nested Relations** | ❌ Not Supported | Only one level of foreign key filtering |
| **Custom Functions** | ❌ Not Supported | No computed fields |
| **Subscriptions** | ❌ Not Supported | Queries and mutations only |
| **Batch Operations** | ❌ Not Supported | One record per mutation |

---

## Troubleshooting

### Empty Results
**Problem:** Query returns `[]` even though data exists

**Solutions:**
- Verify filter values match database format exactly
- Check date format: `YYYY-MM-DD`
- Ensure IDs are integers, not strings
- Remember: string comparisons are case-sensitive

### Relational Filter Not Working
**Problem:** Relational filter doesn't affect results

**Solutions:**
- Ensure JSON is properly escaped
- Verify foreign key field name (e.g., `task_id` not `taskid`)
- Check related table exists and follows naming convention
- Confirm related table has matching records

### Syntax Error
**Problem:** GraphQL syntax error in response

**Solutions:**
- Escape newlines as `\n` in query string
- Properly escape all quotes in JSON
- Validate JSON structure
- Test query in GraphQL playground first

### Authentication Failed
**Problem:** `403 Forbidden` response

**Solutions:**
- Verify `authtoken` header is present
- Check token matches value in database
- Ensure GraphQL module is activated
- Confirm token hasn't been regenerated

---

## Version History

### Version 1.0.1 (Current)
- ✅ Full CRUD operations
- ✅ 8 comparison operators
- ✅ Relational filtering
- ✅ Token authentication
- ✅ Dynamic schema generation
- ✅ Multi-table queries

---

## Support & Resources

- **Documentation:** `GRAPHQL_FILTERING_GUIDE.md`
- **Admin Panel:** `Admin → GraphQL → Token Management`
- **Online Guide:** https://perfexcrm.themesic.com/graphqlguide/
- **Module URI:** https://codecanyon.net/item/perfex-graphql-api-query-all-crms-data-including-custom-modules/54869954

---

**Last Updated:** December 16, 2025  
**Documentation Version:** 1.0  
**Plugin Version:** 1.0.1


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


# GraphQL Plugin Documentation

## 📚 Documentation Overview

This directory contains comprehensive documentation for the Perfex CRM GraphQL Plugin. The documentation is organized into multiple files for easy navigation and reference.

---

## 📖 Documentation Files

### 1. **OPERATIONS_DOCUMENTATION.md** (Main Documentation)
**Complete reference guide covering all operations**

**Contents:**
- Overview and key features
- Authentication methods
- Query operations (read data)
- Mutation operations (create, update, delete)
- Filtering operations (8 comparison operators)
- Relational operations (foreign key filtering)
- Technical implementation details
- API reference and examples
- Best practices and troubleshooting

**Use this when:** You need detailed information about any operation or feature.

---

### 2. **QUICK_REFERENCE.md** (Quick Lookup)
**Fast reference for common operations and syntax**

**Contents:**
- Authentication syntax
- Query templates
- Mutation templates
- Filter operator table
- Common examples
- cURL examples
- Error responses
- Tips and limitations

**Use this when:** You need a quick syntax reminder or example.

---

### 3. **COMPLETE_OPERATIONS_LIST.md** (Structured List)
**Comprehensive structured list of all supported operations**

**Contents:**
- Query operations breakdown
- Mutation operations breakdown
- Filter operations catalog
- Schema operations
- Operation counts and statistics
- Naming conventions
- Capabilities matrix
- Limitations and security

**Use this when:** You need to understand the full scope of available operations.

---

### 4. **OPERATION_FLOW_DIAGRAMS.md** (Visual Guide)
**Visual flowcharts and architecture diagrams**

**Contents:**
- Request flow diagram
- Query resolution flow
- Schema generation flow
- Mutation flow diagrams
- Relational filtering flow
- Type detection flow
- Error handling flow
- Architecture layers
- Component interaction map

**Use this when:** You need to understand how operations work internally.

---

### 5. **GRAPHQL_FILTERING_GUIDE.md** (Existing Guide)
**Original filtering documentation with examples**

**Contents:**
- Basic filtering
- Comparison operators
- Relational filtering
- Advanced examples
- Best practices
- Common use cases
- Troubleshooting

**Use this when:** You need filtering-specific examples and use cases.

---

## 🚀 Quick Start

### Step 1: Authentication
Get your auth token from the admin panel:
```
Admin → GraphQL → Token Management
```

### Step 2: Make Your First Request
```bash
curl -X POST https://your-domain.com/graphql \
  -H "Content-Type: application/json" \
  -H "authtoken: your-token-here" \
  -d '{
    "query": "query {\n  tblstaff {\n    staffid\n    firstname\n    email\n  }\n}"
  }'
```

### Step 3: Explore Operations
- **Read data:** Use queries
- **Create data:** Use `add<TableName>` mutations
- **Update data:** Use `update<TableName>` mutations
- **Delete data:** Use `delete<TableName>` mutations
- **Filter data:** Use operator suffixes (`_eq`, `_gt`, `_like`, etc.)

---

## 📋 Supported Operations Summary

### Core Operations
✅ **Query (Read)** - Fetch data from any table  
✅ **Create (Insert)** - Add new records  
✅ **Update** - Modify existing records  
✅ **Delete** - Remove records  

### Filter Operators (8 Total)
✅ Equal (`_eq`)  
✅ Not Equal (`_ne`)  
✅ Greater Than (`_gt`)  
✅ Greater Than or Equal (`_gte`)  
✅ Less Than (`_lt`)  
✅ Less Than or Equal (`_lte`)  
✅ Like (`_like`)  
✅ In (`_in`)  

### Advanced Features
✅ Multi-table queries  
✅ Relational filtering (foreign keys)  
✅ Dynamic schema generation  
✅ Token authentication  
✅ Automatic type detection  

---

## 🎯 Common Use Cases

### 1. Fetch All Records
```graphql
query {
  tblstaff {
    staffid
    firstname
    email
  }
}
```

### 2. Filter by Date
```graphql
query {
  tbltasks(startdate_eq: "2025-12-12") {
    id
    name
    startdate
  }
}
```

### 3. Date Range Filter
```graphql
query {
  tbltasks(
    startdate_gte: "2025-12-01",
    startdate_lte: "2025-12-31"
  ) {
    id
    name
  }
}
```

### 4. Create Record
```graphql
mutation {
  addTbltasks(
    name: "New Task",
    startdate: "2025-12-15"
  ) {
    id
    message
  }
}
```

### 5. Update Record
```graphql
mutation {
  updateTbltasks(
    id: 123,
    status: "completed"
  ) {
    message
  }
}
```

### 6. Delete Record
```graphql
mutation {
  deleteTbltasks(id: 123) {
    message
  }
}
```

### 7. Relational Filter
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

## 🔑 Key Concepts

### Dynamic Schema
The plugin automatically generates GraphQL schemas for **all database tables**. No manual configuration needed!

### Naming Conventions
- **Queries:** Use exact table name (e.g., `tblstaff`, `tbltasks`)
- **Mutations:** Use `add/update/delete` + PascalCase table name (e.g., `addTblstaff`)
- **Filters:** Use field name + `_` + operator (e.g., `startdate_eq`)

### Type Detection
- Fields named `id` or ending with `_id` → Integer type
- All other fields → String type
- Query results → List of objects

### Foreign Key Mapping
- `task_id` → `tbltasks` or `tbltask`
- `staff_id` → `tblstaffs` or `tblstaff`
- Pattern: `tbl<name>s` or `tbl<name>`

---

## ⚠️ Limitations

❌ **Not Supported:**
- Pagination (LIMIT/OFFSET)
- Sorting (ORDER BY)
- Aggregation (COUNT, SUM, AVG)
- OR logic between filters
- NULL/NOT NULL checks
- Nested relations (beyond one level)
- GraphQL subscriptions
- Batch operations

---

## 🛠️ Troubleshooting

### Empty Results
- Verify filter values match database format
- Check date format: `YYYY-MM-DD`
- Ensure string comparisons match case

### Authentication Failed
- Verify `authtoken` header is present
- Check token matches database value
- Ensure module is activated

### Relational Filter Not Working
- Ensure JSON is properly escaped
- Verify foreign key field name
- Check related table exists

### Syntax Error
- Escape newlines as `\n`
- Properly escape quotes in JSON
- Validate JSON structure

---

## 📊 Documentation Map

```
┌─────────────────────────────────────────────────────────────┐
│                    START HERE                               │
│                                                             │
│  Need quick syntax?  ──────────► QUICK_REFERENCE.md        │
│                                                             │
│  Need detailed info? ──────────► OPERATIONS_DOCUMENTATION.md│
│                                                             │
│  Need complete list? ──────────► COMPLETE_OPERATIONS_LIST.md│
│                                                             │
│  Need visual guide?  ──────────► OPERATION_FLOW_DIAGRAMS.md │
│                                                             │
│  Need filter examples? ────────► GRAPHQL_FILTERING_GUIDE.md │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔗 Additional Resources

- **Admin Panel:** `Admin → GraphQL → Token Management`
- **Online Guide:** https://perfexcrm.themesic.com/graphqlguide/
- **CodeCanyon:** https://codecanyon.net/item/perfex-graphql-api-query-all-crms-data-including-custom-modules/54869954

---

## 📝 Version Information

- **Plugin Version:** 1.0.1
- **Documentation Version:** 1.0
- **Last Updated:** December 16, 2025
- **Minimum Perfex CRM:** 2.9.*

---

## 📧 Support

For issues or questions:
1. Check the relevant documentation file
2. Review the troubleshooting section
3. Test with simple queries first
4. Add complexity incrementally
5. Contact support if needed

---

## 🎓 Learning Path

### Beginner
1. Read **QUICK_REFERENCE.md** for basic syntax
2. Try simple queries from examples
3. Experiment with basic filters

### Intermediate
1. Read **OPERATIONS_DOCUMENTATION.md** for details
2. Try multi-table queries
3. Use relational filtering
4. Combine multiple filters

### Advanced
1. Read **COMPLETE_OPERATIONS_LIST.md** for full scope
2. Study **OPERATION_FLOW_DIAGRAMS.md** for internals
3. Optimize queries for performance
4. Build complex integrations

---

## 📌 Quick Tips

✅ **DO:**
- Request only needed fields
- Use server-side filtering
- Combine multiple filters
- Escape JSON properly

❌ **DON'T:**
- Fetch all fields unnecessarily
- Filter data client-side
- Forget to escape quotes in JSON
- Skip authentication headers

---

## 🎉 Getting Started Checklist

- [ ] Get auth token from admin panel
- [ ] Test basic query with cURL
- [ ] Try filtering with one operator
- [ ] Test create mutation
- [ ] Test update mutation
- [ ] Test delete mutation
- [ ] Try multi-table query
- [ ] Experiment with relational filtering
- [ ] Review best practices
- [ ] Build your integration

---

**Happy Querying! 🚀**


# GraphQL Plugin - Documentation Summary

## 📦 Documentation Package Created

I've created comprehensive documentation for all operations supported by the GraphQL plugin. Here's what was generated:

---

## 📄 Files Created

### 1. **OPERATIONS_DOCUMENTATION.md** (24 KB)
**The main comprehensive documentation**

**Sections:**
- Overview & Key Features
- Authentication (token-based)
- Query Operations (read data)
  - Basic queries
  - Multi-table queries
  - Filtered queries
  - Field selection
- Mutation Operations (create, update, delete)
  - Create/Insert operations
  - Update operations
  - Delete operations
- Filtering Operations (8 operators)
  - Equal, Not Equal
  - Greater Than, Greater/Equal
  - Less Than, Less/Equal
  - Like (pattern matching)
  - In (list matching)
- Relational Operations
  - Foreign key filtering
  - Multi-relation filtering
  - Table mapping patterns
- Technical Implementation
  - Architecture overview
  - Core components
  - Type system
  - Database integration
  - Security features
- API Reference
  - Endpoint details
  - Request/response formats
  - HTTP status codes
  - Example code (cURL, JavaScript, PHP)
- Best Practices & Troubleshooting

---

### 2. **QUICK_REFERENCE.md** (3.4 KB)
**Fast lookup guide for common operations**

**Contents:**
- Authentication syntax
- Query templates
- Mutation templates
- Filter operator table
- Common examples
- cURL example
- Error responses
- Tips (DO's and DON'Ts)
- Limitations list

**Perfect for:** Quick syntax reminders and copy-paste examples

---

### 3. **COMPLETE_OPERATIONS_LIST.md** (15 KB)
**Structured catalog of all operations**

**Sections:**
- Query Operations (detailed breakdown)
- Mutation Operations (detailed breakdown)
- Authentication Operations
- Schema Operations
- Supported Operations by Category
- Operation Counts & Statistics
- Naming Conventions
- Capabilities Matrix
- Operation Examples by Type
- Response Formats
- Limitations (detailed)
- Security Features

**Perfect for:** Understanding the full scope and capabilities

---

### 4. **OPERATION_FLOW_DIAGRAMS.md** (48 KB)
**Visual flowcharts and architecture**

**Diagrams:**
- Complete Request Flow
- Query Resolution Flow
- Schema Generation Flow
- Mutation Flows (Create, Update, Delete)
- Relational Filtering Flow
- Type Detection Flow
- Error Handling Flow
- Request-Response Cycle
- Architecture Layers
- Component Interaction Map

**Perfect for:** Understanding how operations work internally

---

### 5. **README_DOCUMENTATION.md** (9.1 KB)
**Navigation hub for all documentation**

**Contents:**
- Documentation overview
- File descriptions
- Quick start guide
- Supported operations summary
- Common use cases
- Key concepts
- Limitations
- Troubleshooting
- Documentation map
- Learning path
- Getting started checklist

**Perfect for:** Starting point and navigation

---

### 6. **GRAPHQL_FILTERING_GUIDE.md** (11 KB - Existing)
**Original filtering documentation**

**Contents:**
- Basic filtering examples
- Comparison operators
- Relational filtering
- Advanced examples
- Best practices
- Common use cases

**Perfect for:** Filtering-specific examples

---

## 🎯 Operations Documented

### Core CRUD Operations
✅ **Query (Read)** - Fetch data from any database table  
✅ **Create (Insert)** - Add new records to any table  
✅ **Update** - Modify existing records by ID  
✅ **Delete** - Remove records by ID  

### Filter Operations (8 Total)
✅ `_eq` - Equal to  
✅ `_ne` - Not equal to  
✅ `_gt` - Greater than  
✅ `_gte` - Greater than or equal  
✅ `_lt` - Less than  
✅ `_lte` - Less than or equal  
✅ `_like` - Pattern matching (with wildcards)  
✅ `_in` - Match any value in list  

### Advanced Operations
✅ **Multi-table queries** - Query multiple tables in one request  
✅ **Relational filtering** - Filter by foreign key relationships  
✅ **Combined filters** - Use multiple filters with AND logic  
✅ **Dynamic schema** - Auto-generated for all database tables  
✅ **Type detection** - Automatic GraphQL type assignment  

---

## 📊 Coverage Statistics

### Documentation Coverage
- **Total Pages:** 6 markdown files
- **Total Size:** ~110 KB of documentation
- **Total Sections:** 50+ major sections
- **Code Examples:** 100+ examples
- **Diagrams:** 10+ flow diagrams

### Operations Coverage
- **Query Operations:** ✅ Fully documented
- **Mutation Operations:** ✅ Fully documented
- **Filter Operations:** ✅ All 8 operators documented
- **Relational Operations:** ✅ Fully documented
- **Authentication:** ✅ Fully documented
- **Error Handling:** ✅ Fully documented
- **Best Practices:** ✅ Included
- **Troubleshooting:** ✅ Included

---

## 🗺️ Documentation Navigation

```
START HERE: README_DOCUMENTATION.md
    │
    ├─► Need quick syntax?
    │   └─► QUICK_REFERENCE.md
    │
    ├─► Need detailed info?
    │   └─► OPERATIONS_DOCUMENTATION.md
    │
    ├─► Need complete list?
    │   └─► COMPLETE_OPERATIONS_LIST.md
    │
    ├─► Need visual guide?
    │   └─► OPERATION_FLOW_DIAGRAMS.md
    │
    └─► Need filter examples?
        └─► GRAPHQL_FILTERING_GUIDE.md
```

---

## 🎓 Learning Path

### For Beginners
1. Start with **README_DOCUMENTATION.md**
2. Read **QUICK_REFERENCE.md** for syntax
3. Try examples from the quick reference
4. Experiment with basic queries

### For Intermediate Users
1. Read **OPERATIONS_DOCUMENTATION.md** in detail
2. Study filtering operations
3. Try multi-table queries
4. Experiment with relational filtering

### For Advanced Users
1. Review **COMPLETE_OPERATIONS_LIST.md** for full scope
2. Study **OPERATION_FLOW_DIAGRAMS.md** for internals
3. Optimize queries for performance
4. Build complex integrations

---

## 📋 Quick Examples

### Basic Query
```json
{
  "query": "query {\n  tblstaff {\n    staffid\n    firstname\n    email\n  }\n}"
}
```

### Filtered Query
```json
{
  "query": "query {\n  tbltasks(startdate_eq: \"2025-12-12\") {\n    id\n    name\n  }\n}"
}
```

### Create Mutation
```json
{
  "query": "mutation {\n  addTbltasks(name: \"New Task\") {\n    id\n    message\n  }\n}"
}
```

### Update Mutation
```json
{
  "query": "mutation {\n  updateTbltasks(id: 123, status: \"completed\") {\n    message\n  }\n}"
}
```

### Delete Mutation
```json
{
  "query": "mutation {\n  deleteTbltasks(id: 123) {\n    message\n  }\n}"
}
```

---

## 🔑 Key Features Documented

### Dynamic Capabilities
- ✅ Works with **all database tables** automatically
- ✅ Detects **all table fields** automatically
- ✅ Generates **GraphQL schema** dynamically
- ✅ Supports **all CRUD operations** on every table

### Filter Capabilities
- ✅ **8 comparison operators** on all fields
- ✅ **Combine multiple filters** with AND logic
- ✅ **Relational filtering** via foreign keys
- ✅ **Pattern matching** with LIKE operator
- ✅ **List matching** with IN operator

### Security Features
- ✅ **Token authentication** on every request
- ✅ **Module activation** check
- ✅ **SQL injection protection** via Query Builder
- ✅ **CSRF exclusion** for GraphQL endpoint

---

## ⚠️ Documented Limitations

The documentation clearly outlines what is **NOT** supported:

❌ Pagination (LIMIT/OFFSET)  
❌ Sorting (ORDER BY)  
❌ Aggregation (COUNT, SUM, AVG)  
❌ OR logic between filters  
❌ NULL/NOT NULL checks  
❌ Nested relations (beyond one level)  
❌ GraphQL subscriptions  
❌ Batch operations  
❌ Field-level permissions  
❌ Rate limiting  

---

## 📈 Documentation Quality

### Completeness
- ✅ All operations documented
- ✅ All features explained
- ✅ All limitations listed
- ✅ Examples for every operation
- ✅ Troubleshooting guides included

### Clarity
- ✅ Clear section organization
- ✅ Visual diagrams included
- ✅ Code examples provided
- ✅ Tables for quick reference
- ✅ Step-by-step guides

### Usability
- ✅ Multiple documentation formats
- ✅ Quick reference available
- ✅ Detailed explanations available
- ✅ Visual guides available
- ✅ Navigation map provided

---

## 🎯 Use Cases Covered

### Data Retrieval
- ✅ Fetch all records
- ✅ Fetch specific fields
- ✅ Filter by exact match
- ✅ Filter by date range
- ✅ Filter by pattern
- ✅ Filter by list
- ✅ Multi-table queries
- ✅ Relational filtering

### Data Modification
- ✅ Insert new records
- ✅ Update existing records
- ✅ Delete records
- ✅ Get inserted ID
- ✅ Verify updates
- ✅ Confirm deletions

### Advanced Scenarios
- ✅ Daily time reports
- ✅ Employee time tracking
- ✅ Project time analysis
- ✅ Custom field filtering
- ✅ Staff-specific queries
- ✅ Monthly reports

---

## 🚀 Next Steps

### For Users
1. Start with **README_DOCUMENTATION.md**
2. Follow the quick start guide
3. Try the examples
4. Build your integration

### For Developers
1. Review **OPERATION_FLOW_DIAGRAMS.md**
2. Understand the architecture
3. Study the component interactions
4. Extend or customize as needed

---

## 📞 Support Resources

All documentation files include:
- ✅ Troubleshooting sections
- ✅ Common error solutions
- ✅ Best practices
- ✅ Tips and warnings
- ✅ Links to additional resources

---

## ✨ Summary

**What was documented:**
- ✅ 4 core CRUD operations (Query, Create, Update, Delete)
- ✅ 8 filter operators (eq, ne, gt, gte, lt, lte, like, in)
- ✅ Relational filtering capabilities
- ✅ Authentication mechanism
- ✅ Dynamic schema generation
- ✅ Complete API reference
- ✅ Technical implementation details
- ✅ Visual flow diagrams
- ✅ Best practices and troubleshooting

**Documentation formats:**
- ✅ Comprehensive guide (24 KB)
- ✅ Quick reference (3.4 KB)
- ✅ Complete operations list (15 KB)
- ✅ Visual flow diagrams (48 KB)
- ✅ Navigation README (9.1 KB)

**Total documentation:** ~110 KB across 6 files covering every aspect of the GraphQL plugin.

---

**Documentation Version:** 1.0  
**Created:** December 16, 2025  
**Plugin Version:** 1.0.1  
**Status:** ✅ Complete



# Request sample
# Request sample
query {
  __type(name: "Mutation") {
    fields {
      name
    }
  }
}


# Response

{
	"data": {
		"__type": {
			"fields": [
				{
					"name": "addTblactivity_log"
				},
				{
					"name": "updateTblactivity_log"
				},
				{
					"name": "deleteTblactivity_log"
				},
				{
					"name": "addTblannouncements"
				},
				{
					"name": "updateTblannouncements"
				},
				{
					"name": "deleteTblannouncements"
				},
				{
					"name": "addTblclients"
				},
				{
					"name": "updateTblclients"
				},
				{
					"name": "deleteTblclients"
				},
				{
					"name": "addTblconsent_purposes"
				},
				{
					"name": "updateTblconsent_purposes"
				},
				{
					"name": "deleteTblconsent_purposes"
				},
				{
					"name": "addTblconsents"
				},
				{
					"name": "updateTblconsents"
				},
				{
					"name": "deleteTblconsents"
				},
				{
					"name": "addTblcontact_permissions"
				},
				{
					"name": "updateTblcontact_permissions"
				},
				{
					"name": "deleteTblcontact_permissions"
				},
				{
					"name": "addTblcontacts"
				},
				{
					"name": "updateTblcontacts"
				},
				{
					"name": "deleteTblcontacts"
				},
				{
					"name": "addTblcontract_comments"
				},
				{
					"name": "updateTblcontract_comments"
				},
				{
					"name": "deleteTblcontract_comments"
				},
				{
					"name": "addTblcontract_renewals"
				},
				{
					"name": "updateTblcontract_renewals"
				},
				{
					"name": "deleteTblcontract_renewals"
				},
				{
					"name": "addTblcontracts"
				},
				{
					"name": "updateTblcontracts"
				},
				{
					"name": "deleteTblcontracts"
				},
				{
					"name": "addTblcontracts_types"
				},
				{
					"name": "updateTblcontracts_types"
				},
				{
					"name": "deleteTblcontracts_types"
				},
				{
					"name": "addTblcountries"
				},
				{
					"name": "updateTblcountries"
				},
				{
					"name": "deleteTblcountries"
				},
				{
					"name": "addTblcreditnote_refunds"
				},
				{
					"name": "updateTblcreditnote_refunds"
				},
				{
					"name": "deleteTblcreditnote_refunds"
				},
				{
					"name": "addTblcreditnotes"
				},
				{
					"name": "updateTblcreditnotes"
				},
				{
					"name": "deleteTblcreditnotes"
				},
				{
					"name": "addTblcredits"
				},
				{
					"name": "updateTblcredits"
				},
				{
					"name": "deleteTblcredits"
				},
				{
					"name": "addTblcurrencies"
				},
				{
					"name": "updateTblcurrencies"
				},
				{
					"name": "deleteTblcurrencies"
				},
				{
					"name": "addTblcustomer_admins"
				},
				{
					"name": "updateTblcustomer_admins"
				},
				{
					"name": "deleteTblcustomer_admins"
				},
				{
					"name": "addTblcustomer_groups"
				},
				{
					"name": "updateTblcustomer_groups"
				},
				{
					"name": "deleteTblcustomer_groups"
				},
				{
					"name": "addTblcustomers_groups"
				},
				{
					"name": "updateTblcustomers_groups"
				},
				{
					"name": "deleteTblcustomers_groups"
				},
				{
					"name": "addTblcustomfields"
				},
				{
					"name": "updateTblcustomfields"
				},
				{
					"name": "deleteTblcustomfields"
				},
				{
					"name": "addTblcustomfieldsvalues"
				},
				{
					"name": "updateTblcustomfieldsvalues"
				},
				{
					"name": "deleteTblcustomfieldsvalues"
				},
				{
					"name": "addTbldepartments"
				},
				{
					"name": "updateTbldepartments"
				},
				{
					"name": "deleteTbldepartments"
				},
				{
					"name": "addTbldismissed_announcements"
				},
				{
					"name": "updateTbldismissed_announcements"
				},
				{
					"name": "deleteTbldismissed_announcements"
				},
				{
					"name": "addTblemaillists"
				},
				{
					"name": "updateTblemaillists"
				},
				{
					"name": "deleteTblemaillists"
				},
				{
					"name": "addTblemailtemplates"
				},
				{
					"name": "updateTblemailtemplates"
				},
				{
					"name": "deleteTblemailtemplates"
				},
				{
					"name": "addTblestimate_request_forms"
				},
				{
					"name": "updateTblestimate_request_forms"
				},
				{
					"name": "deleteTblestimate_request_forms"
				},
				{
					"name": "addTblestimate_request_status"
				},
				{
					"name": "updateTblestimate_request_status"
				},
				{
					"name": "deleteTblestimate_request_status"
				},
				{
					"name": "addTblestimate_requests"
				},
				{
					"name": "updateTblestimate_requests"
				},
				{
					"name": "deleteTblestimate_requests"
				},
				{
					"name": "addTblestimates"
				},
				{
					"name": "updateTblestimates"
				},
				{
					"name": "deleteTblestimates"
				},
				{
					"name": "addTblevents"
				},
				{
					"name": "updateTblevents"
				},
				{
					"name": "deleteTblevents"
				},
				{
					"name": "addTblexpenses"
				},
				{
					"name": "updateTblexpenses"
				},
				{
					"name": "deleteTblexpenses"
				},
				{
					"name": "addTblexpenses_categories"
				},
				{
					"name": "updateTblexpenses_categories"
				},
				{
					"name": "deleteTblexpenses_categories"
				},
				{
					"name": "addTblfiles"
				},
				{
					"name": "updateTblfiles"
				},
				{
					"name": "deleteTblfiles"
				},
				{
					"name": "addTblfilter_defaults"
				},
				{
					"name": "updateTblfilter_defaults"
				},
				{
					"name": "deleteTblfilter_defaults"
				},
				{
					"name": "addTblfilters"
				},
				{
					"name": "updateTblfilters"
				},
				{
					"name": "deleteTblfilters"
				},
				{
					"name": "addTblform_question_box"
				},
				{
					"name": "updateTblform_question_box"
				},
				{
					"name": "deleteTblform_question_box"
				},
				{
					"name": "addTblform_question_box_description"
				},
				{
					"name": "updateTblform_question_box_description"
				},
				{
					"name": "deleteTblform_question_box_description"
				},
				{
					"name": "addTblform_questions"
				},
				{
					"name": "updateTblform_questions"
				},
				{
					"name": "deleteTblform_questions"
				},
				{
					"name": "addTblform_results"
				},
				{
					"name": "updateTblform_results"
				},
				{
					"name": "deleteTblform_results"
				},
				{
					"name": "addTblgdpr_requests"
				},
				{
					"name": "updateTblgdpr_requests"
				},
				{
					"name": "deleteTblgdpr_requests"
				},
				{
					"name": "addTblgoals"
				},
				{
					"name": "updateTblgoals"
				},
				{
					"name": "deleteTblgoals"
				},
				{
					"name": "addTblinvoicepaymentrecords"
				},
				{
					"name": "updateTblinvoicepaymentrecords"
				},
				{
					"name": "deleteTblinvoicepaymentrecords"
				},
				{
					"name": "addTblinvoices"
				},
				{
					"name": "updateTblinvoices"
				},
				{
					"name": "deleteTblinvoices"
				},
				{
					"name": "addTblitem_tax"
				},
				{
					"name": "updateTblitem_tax"
				},
				{
					"name": "deleteTblitem_tax"
				},
				{
					"name": "addTblitemable"
				},
				{
					"name": "updateTblitemable"
				},
				{
					"name": "deleteTblitemable"
				},
				{
					"name": "addTblitems"
				},
				{
					"name": "updateTblitems"
				},
				{
					"name": "deleteTblitems"
				},
				{
					"name": "addTblitems_groups"
				},
				{
					"name": "updateTblitems_groups"
				},
				{
					"name": "deleteTblitems_groups"
				},
				{
					"name": "addTblknowedge_base_article_feedback"
				},
				{
					"name": "updateTblknowedge_base_article_feedback"
				},
				{
					"name": "deleteTblknowedge_base_article_feedback"
				},
				{
					"name": "addTblknowledge_base"
				},
				{
					"name": "updateTblknowledge_base"
				},
				{
					"name": "deleteTblknowledge_base"
				},
				{
					"name": "addTblknowledge_base_groups"
				},
				{
					"name": "updateTblknowledge_base_groups"
				},
				{
					"name": "deleteTblknowledge_base_groups"
				},
				{
					"name": "addTbllead_activity_log"
				},
				{
					"name": "updateTbllead_activity_log"
				},
				{
					"name": "deleteTbllead_activity_log"
				},
				{
					"name": "addTbllead_integration_emails"
				},
				{
					"name": "updateTbllead_integration_emails"
				},
				{
					"name": "deleteTbllead_integration_emails"
				},
				{
					"name": "addTblleads"
				},
				{
					"name": "updateTblleads"
				},
				{
					"name": "deleteTblleads"
				},
				{
					"name": "addTblleads_email_integration"
				},
				{
					"name": "updateTblleads_email_integration"
				},
				{
					"name": "deleteTblleads_email_integration"
				},
				{
					"name": "addTblleads_sources"
				},
				{
					"name": "updateTblleads_sources"
				},
				{
					"name": "deleteTblleads_sources"
				},
				{
					"name": "addTblleads_status"
				},
				{
					"name": "updateTblleads_status"
				},
				{
					"name": "deleteTblleads_status"
				},
				{
					"name": "addTbllistemails"
				},
				{
					"name": "updateTbllistemails"
				},
				{
					"name": "deleteTbllistemails"
				},
				{
					"name": "addTblmail_queue"
				},
				{
					"name": "updateTblmail_queue"
				},
				{
					"name": "deleteTblmail_queue"
				},
				{
					"name": "addTblmaillistscustomfields"
				},
				{
					"name": "updateTblmaillistscustomfields"
				},
				{
					"name": "deleteTblmaillistscustomfields"
				},
				{
					"name": "addTblmaillistscustomfieldvalues"
				},
				{
					"name": "updateTblmaillistscustomfieldvalues"
				},
				{
					"name": "deleteTblmaillistscustomfieldvalues"
				},
				{
					"name": "addTblmigrations"
				},
				{
					"name": "updateTblmigrations"
				},
				{
					"name": "deleteTblmigrations"
				},
				{
					"name": "addTblmilestones"
				},
				{
					"name": "updateTblmilestones"
				},
				{
					"name": "deleteTblmilestones"
				},
				{
					"name": "addTblmodules"
				},
				{
					"name": "updateTblmodules"
				},
				{
					"name": "deleteTblmodules"
				},
				{
					"name": "addTblnewsfeed_comment_likes"
				},
				{
					"name": "updateTblnewsfeed_comment_likes"
				},
				{
					"name": "deleteTblnewsfeed_comment_likes"
				},
				{
					"name": "addTblnewsfeed_post_comments"
				},
				{
					"name": "updateTblnewsfeed_post_comments"
				},
				{
					"name": "deleteTblnewsfeed_post_comments"
				},
				{
					"name": "addTblnewsfeed_post_likes"
				},
				{
					"name": "updateTblnewsfeed_post_likes"
				},
				{
					"name": "deleteTblnewsfeed_post_likes"
				},
				{
					"name": "addTblnewsfeed_posts"
				},
				{
					"name": "updateTblnewsfeed_posts"
				},
				{
					"name": "deleteTblnewsfeed_posts"
				},
				{
					"name": "addTblnotes"
				},
				{
					"name": "updateTblnotes"
				},
				{
					"name": "deleteTblnotes"
				},
				{
					"name": "addTblnotifications"
				},
				{
					"name": "updateTblnotifications"
				},
				{
					"name": "deleteTblnotifications"
				},
				{
					"name": "addTbloptions"
				},
				{
					"name": "updateTbloptions"
				},
				{
					"name": "deleteTbloptions"
				},
				{
					"name": "addTblpayment_attempts"
				},
				{
					"name": "updateTblpayment_attempts"
				},
				{
					"name": "deleteTblpayment_attempts"
				},
				{
					"name": "addTblpayment_modes"
				},
				{
					"name": "updateTblpayment_modes"
				},
				{
					"name": "deleteTblpayment_modes"
				},
				{
					"name": "addTblpinned_projects"
				},
				{
					"name": "updateTblpinned_projects"
				},
				{
					"name": "deleteTblpinned_projects"
				},
				{
					"name": "addTblproject_activity"
				},
				{
					"name": "updateTblproject_activity"
				},
				{
					"name": "deleteTblproject_activity"
				},
				{
					"name": "addTblproject_files"
				},
				{
					"name": "updateTblproject_files"
				},
				{
					"name": "deleteTblproject_files"
				},
				{
					"name": "addTblproject_members"
				},
				{
					"name": "updateTblproject_members"
				},
				{
					"name": "deleteTblproject_members"
				},
				{
					"name": "addTblproject_notes"
				},
				{
					"name": "updateTblproject_notes"
				},
				{
					"name": "deleteTblproject_notes"
				},
				{
					"name": "addTblproject_settings"
				},
				{
					"name": "updateTblproject_settings"
				},
				{
					"name": "deleteTblproject_settings"
				},
				{
					"name": "addTblprojectdiscussioncomments"
				},
				{
					"name": "updateTblprojectdiscussioncomments"
				},
				{
					"name": "deleteTblprojectdiscussioncomments"
				},
				{
					"name": "addTblprojectdiscussions"
				},
				{
					"name": "updateTblprojectdiscussions"
				},
				{
					"name": "deleteTblprojectdiscussions"
				},
				{
					"name": "addTblprojects"
				},
				{
					"name": "updateTblprojects"
				},
				{
					"name": "deleteTblprojects"
				},
				{
					"name": "addTblproposal_comments"
				},
				{
					"name": "updateTblproposal_comments"
				},
				{
					"name": "deleteTblproposal_comments"
				},
				{
					"name": "addTblproposals"
				},
				{
					"name": "updateTblproposals"
				},
				{
					"name": "deleteTblproposals"
				},
				{
					"name": "addTblrelated_items"
				},
				{
					"name": "updateTblrelated_items"
				},
				{
					"name": "deleteTblrelated_items"
				},
				{
					"name": "addTblreminders"
				},
				{
					"name": "updateTblreminders"
				},
				{
					"name": "deleteTblreminders"
				},
				{
					"name": "addTblroles"
				},
				{
					"name": "updateTblroles"
				},
				{
					"name": "deleteTblroles"
				},
				{
					"name": "addTblsales_activity"
				},
				{
					"name": "updateTblsales_activity"
				},
				{
					"name": "deleteTblsales_activity"
				},
				{
					"name": "addTblscheduled_emails"
				},
				{
					"name": "updateTblscheduled_emails"
				},
				{
					"name": "deleteTblscheduled_emails"
				},
				{
					"name": "addTblservices"
				},
				{
					"name": "updateTblservices"
				},
				{
					"name": "deleteTblservices"
				},
				{
					"name": "addTblsessions"
				},
				{
					"name": "updateTblsessions"
				},
				{
					"name": "deleteTblsessions"
				},
				{
					"name": "addTblshared_customer_files"
				},
				{
					"name": "updateTblshared_customer_files"
				},
				{
					"name": "deleteTblshared_customer_files"
				},
				{
					"name": "addTblspam_filters"
				},
				{
					"name": "updateTblspam_filters"
				},
				{
					"name": "deleteTblspam_filters"
				},
				{
					"name": "addTblstaff"
				},
				{
					"name": "updateTblstaff"
				},
				{
					"name": "deleteTblstaff"
				},
				{
					"name": "addTblstaff_departments"
				},
				{
					"name": "updateTblstaff_departments"
				},
				{
					"name": "deleteTblstaff_departments"
				},
				{
					"name": "addTblstaff_permissions"
				},
				{
					"name": "updateTblstaff_permissions"
				},
				{
					"name": "deleteTblstaff_permissions"
				},
				{
					"name": "addTblsubscriptions"
				},
				{
					"name": "updateTblsubscriptions"
				},
				{
					"name": "deleteTblsubscriptions"
				},
				{
					"name": "addTblsurveyresultsets"
				},
				{
					"name": "updateTblsurveyresultsets"
				},
				{
					"name": "deleteTblsurveyresultsets"
				},
				{
					"name": "addTblsurveys"
				},
				{
					"name": "updateTblsurveys"
				},
				{
					"name": "deleteTblsurveys"
				},
				{
					"name": "addTblsurveysemailsendcron"
				},
				{
					"name": "updateTblsurveysemailsendcron"
				},
				{
					"name": "deleteTblsurveysemailsendcron"
				},
				{
					"name": "addTblsurveysendlog"
				},
				{
					"name": "updateTblsurveysendlog"
				},
				{
					"name": "deleteTblsurveysendlog"
				},
				{
					"name": "addTbltaggables"
				},
				{
					"name": "updateTbltaggables"
				},
				{
					"name": "deleteTbltaggables"
				},
				{
					"name": "addTbltags"
				},
				{
					"name": "updateTbltags"
				},
				{
					"name": "deleteTbltags"
				},
				{
					"name": "addTbltask_assigned"
				},
				{
					"name": "updateTbltask_assigned"
				},
				{
					"name": "deleteTbltask_assigned"
				},
				{
					"name": "addTbltask_checklist_items"
				},
				{
					"name": "updateTbltask_checklist_items"
				},
				{
					"name": "deleteTbltask_checklist_items"
				},
				{
					"name": "addTbltask_comments"
				},
				{
					"name": "updateTbltask_comments"
				},
				{
					"name": "deleteTbltask_comments"
				},
				{
					"name": "addTbltask_followers"
				},
				{
					"name": "updateTbltask_followers"
				},
				{
					"name": "deleteTbltask_followers"
				},
				{
					"name": "addTbltasks"
				},
				{
					"name": "updateTbltasks"
				},
				{
					"name": "deleteTbltasks"
				},
				{
					"name": "addTbltasks_checklist_templates"
				},
				{
					"name": "updateTbltasks_checklist_templates"
				},
				{
					"name": "deleteTbltasks_checklist_templates"
				},
				{
					"name": "addTbltaskstimers"
				},
				{
					"name": "updateTbltaskstimers"
				},
				{
					"name": "deleteTbltaskstimers"
				},
				{
					"name": "addTbltaxes"
				},
				{
					"name": "updateTbltaxes"
				},
				{
					"name": "deleteTbltaxes"
				},
				{
					"name": "addTbltemplates"
				},
				{
					"name": "updateTbltemplates"
				},
				{
					"name": "deleteTbltemplates"
				},
				{
					"name": "addTblticket_attachments"
				},
				{
					"name": "updateTblticket_attachments"
				},
				{
					"name": "deleteTblticket_attachments"
				},
				{
					"name": "addTblticket_replies"
				},
				{
					"name": "updateTblticket_replies"
				},
				{
					"name": "deleteTblticket_replies"
				},
				{
					"name": "addTbltickets"
				},
				{
					"name": "updateTbltickets"
				},
				{
					"name": "deleteTbltickets"
				},
				{
					"name": "addTbltickets_pipe_log"
				},
				{
					"name": "updateTbltickets_pipe_log"
				},
				{
					"name": "deleteTbltickets_pipe_log"
				},
				{
					"name": "addTbltickets_predefined_replies"
				},
				{
					"name": "updateTbltickets_predefined_replies"
				},
				{
					"name": "deleteTbltickets_predefined_replies"
				},
				{
					"name": "addTbltickets_priorities"
				},
				{
					"name": "updateTbltickets_priorities"
				},
				{
					"name": "deleteTbltickets_priorities"
				},
				{
					"name": "addTbltickets_status"
				},
				{
					"name": "updateTbltickets_status"
				},
				{
					"name": "deleteTbltickets_status"
				},
				{
					"name": "addTbltodos"
				},
				{
					"name": "updateTbltodos"
				},
				{
					"name": "deleteTbltodos"
				},
				{
					"name": "addTbltracked_mails"
				},
				{
					"name": "updateTbltracked_mails"
				},
				{
					"name": "deleteTbltracked_mails"
				},
				{
					"name": "addTbltwocheckout_log"
				},
				{
					"name": "updateTbltwocheckout_log"
				},
				{
					"name": "deleteTbltwocheckout_log"
				},
				{
					"name": "addTbluser_auto_login"
				},
				{
					"name": "updateTbluser_auto_login"
				},
				{
					"name": "deleteTbluser_auto_login"
				},
				{
					"name": "addTbluser_meta"
				},
				{
					"name": "updateTbluser_meta"
				},
				{
					"name": "deleteTbluser_meta"
				},
				{
					"name": "addTblvault"
				},
				{
					"name": "updateTblvault"
				},
				{
					"name": "deleteTblvault"
				},
				{
					"name": "addTblviews_tracking"
				},
				{
					"name": "updateTblviews_tracking"
				},
				{
					"name": "deleteTblviews_tracking"
				},
				{
					"name": "addTblweb_to_lead"
				},
				{
					"name": "updateTblweb_to_lead"
				},
				{
					"name": "deleteTblweb_to_lead"
				}
			]
		}
	}
}