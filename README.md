# Code Meta

[![Release](https://img.shields.io/badge/Release-v1.0.0-blue.svg)](https://github.com/YuetChan/code-meta/releases/tag/v1.0.0)
[![Build](https://img.shields.io/badge/Build-Passing-brightgreen.svg)](https://github.com/YuetChan/code-meta)
[![Issue](https://img.shields.io/github/issues/YuetChan/code-meta)](https://github.com/YuetChan/code-meta/issues)
[![License](https://img.shields.io/badge/License-GPL-yellow.svg)](https://github.com/YuetChan/code-meta/blob/main/LICENSE)

This is a note-taking app that allows developers to easily manage, edit and share notes associated with files in a project.

![CodeMetaScreenshot](https://i.ibb.co/cJ0RBQ3/Screenshot-from-2023-04-13-00-32-03.png)

## Dependencies

The following dependencies are required to run the Project Name application:

- Python 3.8 +
- PyQt5 `sudo apt-get install python3-pyqt5`

## Installation

1. Clone the Code Meta repository: `git clone https://github.com/YuetChan/code-meta.git`
2. Change to the code-meta directory: `cd /path/to/code-meta`
3. Make the build.sh script executable: `chmod +x ./build.sh`
4. Run the script: `./build.sh`
5. Code Meta icon should show up on show applications/application menu

## Usage

- Open existing projects: Users can open an existing project by selecting the project folder, and then choosing the existing datasource file that contains the note data.
- Create new projects: Users can create a new project by choosing a project folder, which will generate a datasource file that contains note data associated with the files in the folder. 
- File tree and text editor: Once a project is opened or created, users can view a file tree and a text editor for editing notes associated with files.
- Dangling file searcher: The application provides a search bar and a file list that displays files with dangling notes, which are notes associated with files that are not present in the file tree.
- Auto deletion: When users empty dangling notes, it will remove the associated file from the file list.
- Add notes from a datasource file: Users can add other people's notes by choosing a datasource file.


## License

This project is licensed under the GPL License - see the [LICENSE](https://github.com/YuetChan/code-meta/blob/master/LICENSE)
 file for details.

## Contact Information

For any questions or inquiries, please contact Yuet Chan at yuetcheukchan@gmail.com.
