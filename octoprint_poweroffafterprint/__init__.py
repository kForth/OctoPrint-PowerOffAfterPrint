import octoprint.plugin
from octoprint.events import Events


class State:
    ENABLED = True
    DISABLED = False
    UNCHANGED = None


class PowerOffAfterPrintPlugin(
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.EventHandlerPlugin,
):
    def __init__(self):
        super().__init__()

        defaults = self.get_settings_defaults()
        self._powerOffScript = defaults["powerOffScript"]
        self._powerOffOnDone = defaults["powerOffOnDone"]
        self._powerOffOnFail = defaults["powerOffOnFail"]
        self._powerOffOnCancel = defaults["powerOffOnCancel"]
        self._stateAfterStartup = defaults["stateAfterStartup"]
        self._stateAfterPrintStart = defaults["stateAfterPrintStart"]
        self._stateAfterPrintDone = defaults["stateAfterPrintDone"]
        self._enabled = defaults["enabled"]

    def _power_off(self, event):
        self._logger.warn("Power Off Printer on %s: %s", event, self._powerOffScript)
        self._printer.commands([self._powerOffScript])
        self._printer.disconnect()

    def _update_client_settings(self):
        self._plugin_manager.send_plugin_message(
            self._identifier,
            {
                "settings": {
                    "powerOffScript": self._powerOffScript,
                    "powerOffOnDone": self._powerOffOnDone,
                    "powerOffOnFail": self._powerOffOnFail,
                    "powerOffOnCancel": self._powerOffOnCancel,
                    "stateAfterStartup": self._stateAfterStartup,
                    "stateAfterPrintStart": self._stateAfterPrintStart,
                    "stateAfterPrintDone": self._stateAfterPrintDone,
                    "enabled": self._enabled,
                }
            },
        )

    ##~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return {
            "powerOffScript": "M81",
            "powerOffOnDone": True,
            "powerOffOnFail": True,
            "powerOffOnCancel": False,
            "stateAfterStartup": State.DISABLED,
            "stateAfterPrintStart": State.UNCHANGED,
            "stateAfterPrintDone": State.DISABLED,
            "enabled": State.DISABLED,
        }

    def on_settings_save(self, data):
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        self.read_settings()
        self._update_client_settings()

    def read_settings(self):
        self._powerOffScript = self._settings.get(["powerOffScript"])
        self._powerOffOnDone = self._settings.getBoolean(["powerOffOnDone"])
        self._powerOffOnFail = self._settings.getBoolean(["powerOffOnFail"])
        self._powerOffOnCancel = self._settings.getBoolean(["powerOffOnCancel"])
        self._stateAfterStartup = self._settings.getBoolean(["stateAfterStartup"])
        self._stateAfterPrintStart = self._settings.getBoolean(["stateAfterPrintStart"])
        self._stateAfterPrintDone = self._settings.getBoolean(["stateAfterPrintDone"])
        self._enabled = self._settings.getBoolean(["enabled"])

    def write_settings(self):
        self._settings.set(["powerOffScript"], self._powerOffScript)
        self._settings.setBoolean(["powerOffOnDone"], self._powerOffOnDone)
        self._settings.setBoolean(["powerOffOnFail"], self._powerOffOnFail)
        self._settings.setBoolean(["powerOffOnCancel"], self._powerOffOnCancel)
        self._settings.setBoolean(["stateAfterStartup"], self._stateAfterStartup)
        self._settings.setBoolean(["stateAfterPrintStart"], self._stateAfterPrintStart)
        self._settings.setBoolean(["stateAfterPrintDone"], self._stateAfterPrintDone)
        self._settings.setBoolean(["enabled"], self._enabled)
        self._settings.save()

    ##~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return {"js": ["js/poweroffafterprint.js"]}

    ##~~ TemplatePlugin mixin

    def get_template_configs(self):
        return [
            {
                "type": "settings",
                "name": "PowerOffAfterPrint Plugin",
                "template": "poweroffafterprint_settings.jinja2",
                "custom_bindings": True,
            },
            {
                "type": "sidebar",
                "name": "Power Off After Print",
                "template": "poweroffafterprint_sidebar.jinja2",
                "custom_bindings": True,
                "icon": "fas fa-power-off",
            },
        ]

    ##~~ StartupPlugin mixin

    def on_after_startup(self):
        self.read_settings()
        if self._stateAfterStartup != State.UNCHANGED:
            self._enabled = self._stateAfterStartup
            self.write_settings()
        return super().on_after_startup()

    ##~~ EventHandlerPlugin mixin

    def on_event(self, event, payload):
        if event not in (Events.PRINT_STARTED, Events.PRINT_FAILED, Events.PRINT_DONE):
            return

        if event == Events.PRINT_STARTED:
            if self._stateAfterPrintStart != State.UNCHANGED:
                self._enabled = self._stateAfterPrintStart
                self.write_settings()

        else:  # event == Events.PRINT_DONE or event == Events.PRINT_FAILED
            if self._enabled:
                if event == Events.PRINT_DONE:
                    if self._powerOffOnDone:
                        self._power_off(event)
                else:  # event == Events.PRINT_FAILED:
                    if self._powerOffOnCancel:
                        if payload.get("reason", False) == "cancelled":
                            self._power_off(event)
                    elif self._powerOffOnFail:
                        self._power_off(event)

            if self._stateAfterPrintDone != State.UNCHANGED:
                self._enabled = self._stateAfterPrintDone
                self.write_settings()

    ##~~ SoftwareUpdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return {
            "poweroffafterprint": {
                "displayName": "PowerOffAfterPrint Plugin",
                "displayVersion": self._plugin_version,
                # version check: github repository
                "type": "github_release",
                "user": "kforth",
                "repo": "OctoPrint-PowerOffAfterPrint",
                "current": self._plugin_version,
                # update method: pip
                "pip": "https://github.com/kforth/OctoPrint-PowerOffAfterPrint/archive/{target_version}.zip",
            }
        }


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "PowerOffAfterPrint Plugin"


# Set the Python version your plugin is compatible with below. Recommended is Python 3 only for all new plugins.
# OctoPrint 1.4.0 - 1.7.x run under both Python 3 and the end-of-life Python 2.
# OctoPrint 1.8.0 onwards only supports Python 3.
__plugin_pythoncompat__ = ">=3,<4"  # Only Python 3


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = PowerOffAfterPrintPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
