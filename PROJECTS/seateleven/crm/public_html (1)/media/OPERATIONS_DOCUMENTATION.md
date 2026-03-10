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
