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
