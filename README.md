# OctoPrint-PowerOffAfterPrint

Automatically shutdown your 3D Printer after a print is done.

## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

`https://github.com/kforth/OctoPrint-PowerOffAfterPrint/archive/main.zip`

## Configuration

After installation, open OctoPrint settings (wrench icon) and scroll down to the "PowerOffAfterPrint Plugin" page.

You can configure the following options:

| Option | Default | Description |
|:-------|:--------|:------------|
|`Power Off Script`| M81 | The commands sent to the printer to shutdown. |
|`Power Off On Done`| True | Power off the printer if the print was successful. |
|`Power Off On Fail`| True | Power off the printer if the print failed. |
|`State On Startup`| Disabled | Initial state for plugin when OctoPrint starts. |
|`State On Print Start`| Unchanged | Automatically set the current state when a print is started. |
|`State On Print End`| Disabled | Automatically set the current state when a print is finished. |

## Screenshots

### Sidebar
![Sidebar Screenshot](https://raw.githubusercontent.com/kForth/plugins.octoprint.org/register/poweroffafterprint/assets/img/plugins/poweroffafterprint/sidebar_enabled.png)

![Sidebar Screenshot](https://raw.githubusercontent.com/kForth/plugins.octoprint.org/register/poweroffafterprint/assets/img/plugins/poweroffafterprint/sidebar_disabled.png)

### Settings Page
![Settings Screenshot](https://raw.githubusercontent.com/kForth/plugins.octoprint.org/register/poweroffafterprint/assets/img/plugins/poweroffafterprint/settings.png)

## License

Copyright © 2022 [Kestin Goforth](https://github.com/kforth/).

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the [GNU Affero General Public License](https://www.gnu.org/licenses/agpl-3.0.en.html) for more details.
