# markdown-parser
My python scripts to parse Markdown.

### Table-Parser
The md_table_parser parses markdown tables and returns the result as table objects. 
The required table format is:
```
## Name of the table

Optional description

|colum name 1|colum name 2|...|
|---|---|...|
| row 1.1 | row 1.2 |...|
| row 2.1 | row 2.2 |...|
...
```
Empty lines and "empty" rows (like ```| | | |```) will be ignored. The table object has a pretty print method to, you guessed it, pretty print the table. It has a filter function too. This function takes a criteria function and e only the rows for which the criteria function evaluates true.
