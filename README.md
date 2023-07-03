# Repository Management Tool

This tool provides functionalities for managing repositories.

## Endpoints

- **Run Commands**: Execute a command and retrieve the output.

  - URL: `http://127.0.0.1:8000/run-commands/?command=(command_name)`

- **List Logs**: Get a list of available logs.

  - URL: `http://127.0.0.1:8000/list-outputs/`

- **Filter by Commands**: Filter commands by command name.

  - URL: `http://127.0.0.1:8000/filter-by-commands/?command=(command_name)`

- **Get Command Output**: Get the output of a specific command by ID.

  - URL: `http://127.0.0.1:8000/filter-by-commands/(id_num)` (Trailing slash at the end is optional)

- **Filter by Date**: Filter commands by the number of days.

  - URL: `http://127.0.0.1:8000/filter-by-date/?num_days=(int_days_num)`

- **Get Command by ID**: Get a specific command by ID.

  - URL: `http://127.0.0.1:8000/filter-by-date/(id_num)` (Trailing slash at the end is optional)

- **Filter by Status**: Filter commands by status.

  - URL: `http://127.0.0.1:8000/filter-by-status/?status=(0_or_1)`

- **Get Command by ID**: Get a specific command by ID.

  - URL: `http://127.0.0.1:8000/filter-by-status/(id_num)` (Trailing slash at the end is optional)

- **Running Commands**: Display currently running threads.

  - URL: `http://127.0.0.1:8000/running-commands/`

