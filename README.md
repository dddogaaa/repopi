# Repository Management Tool

This application is crafted to enhance user convenience with functionalities for repository management through `APTLY` commands.

**Capabilities:**

- Use specific commands from the web interface with a single click.
- Browse and filter the logs by status and command name from the web interface.
- Most notably, users have the ability to view real-time output while processes are ongoing. Furthermore, the application offers the capability to display outputs for both successful and erroneous transactions, ensuring a smooth and transparent experience.


<!-- This will be provide functionalities for managing repositories using Aptly commands. -->

## Installation
- **Install APTLY**

  Debian/Ubuntu:
  
  Aptly could be installed by adding new repository to ```/etc/apt/sources.list```:

  ``` # deb http://repo.aptly.info/ squeeze main ```

  And importing key that is used to sign the release either from keyserver.ubuntu.com:

  ``` $ wget -qO - https://www.aptly.info/pubkey.txt | sudo apt-key add - ```

  After that you can install aptly as any other software package:

  ```bash
    # apt-get update
    # apt-get install aptly
  ```

  - Note: Please don't worry about ```squeeze``` part in repo name: aptly package should work on Debian squeeze+,          Ubuntu 10.0+. Package contains aptly binary, man page and bash completion.
    
    If you would like to use nightly (unstable) builds of aptly, add following line to ```/etc/apt/sources.list```:

    ```bash deb http://repo.aptly.info/ nightly main ```

  MacOS: Installation using Homebrew:
    
  ```bash $ brew install aptly ```
   
   

   
- **Install requirements.**

  ```pip install -r requirements.txt```
  
- **Start django server.**
  
  ```python manage.py runserver ```
  
<br>

*IMPORTANT NOTE:* Change the linux and mac parts on commandTool/views.py according to your OS. 


## Log File

- Logs file folder path inside in repopi/settings.py as *DATA_FOLDER*

  Ex: DATA_FOLDER = "/tmp/"

  
## Example Usage
<br>

<img src="demo.gif"/>

<br>



