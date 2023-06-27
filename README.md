# Repository Management Tool

This tool provides functionalities for managing repositories.

## Endpoints

- **Run Commands**: Execute a command and retrieve the output.

  - URL: `http://127.0.0.1:8000/run-commands/?command=ls`

- **List Logs**: Get a list of available logs.

  - URL: `http://127.0.0.1:8000/list-logs/`

- **Filter by Commands**: Filter commands by command name.

  - URL: `http://127.0.0.1:8000/filter-by-commands/?command=ls`

- **Get Command Output**: Get the output of a specific command by ID.

  - URL: `http://127.0.0.1:8000/filter-by-commands/(id_num)` (Trailing slash at the end is optional)

- **Filter by Date**: Filter commands by the number of days.

  - URL: `http://127.0.0.1:8000/filter-by-date/?num_days=3`

- **Get Command by ID**: Get a specific command by ID.

  - URL: `http://127.0.0.1:8000/filter-by-date/(id_num)`

- **Filter by Status**: Filter commands by status.

  - URL: `http://127.0.0.1:8000/filter-by-status/?status=0`

- **Get Command by ID**: Get a specific command by ID.

  - URL: `http://127.0.0.1:8000/filter-by-status/(id_num)` (Trailing slash at the end is optional)

