# Repository Management Tool

This tool provides functionalities for managing repositories.

The outputs of commands are saved in ../Desktop/repopi_outputs. The path can be changeable in setting.py.

## Endpoints

- **Run Commands**: Execute a command.

  - URL: `http://127.0.0.1:8000/run/?command=(command_name)`

- **List Logs**: Get a list of available logs.

  - URL: `http://127.0.0.1:8000/list-outputs/`

- **Filter by Commands**: Filter commands by command name.

  - URL: `http://127.0.0.1:8000/filter-commands/?command=(command_name)`
  - URL: `http://127.0.0.1:8000/filter-commands/?status=(0_1_2)`

- **Get Command by ID**: Get a specific output by ID.

  - URL: `http://127.0.0.1:8000/filter-commands/(id_num)`

