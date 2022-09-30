/*
 * View model for OctoPrint-PowerOffAfterPrint
 *
 * Author: Kestin Goforth
 * License: AGPLv3
 */
$(function () {
    function PowerOffAfterPrintViewModel(parameters) {
        const PLUGIN_ID = "poweroffafterprint";

        var self = this;

        self.states = {Enabled: true, Disabled: false, Unchanged: null};
        self.stateOptions = ko.observableArray(["Enabled", "Disabled", "Unchanged"]);

        self.settingsView = parameters[0];

        self.powerOffScript = ko.observable(undefined);
        self.powerOffOnDone = ko.observable(undefined);
        self.powerOffOnFail = ko.observable(undefined);
        self.powerOffOnCancel = ko.observable(undefined);
        self.stateAfterStartup = ko.observable(undefined);
        self.stateAfterPrintStart = ko.observable(undefined);
        self.stateAfterPrintDone = ko.observable(undefined);
        self.enabled = ko.observable(false);

        self._selectedStateAfterStartup = ko.observable(undefined);
        self._selectedStateAfterPrintStart = ko.observable(undefined);
        self._selectedStateAfterPrintDone = ko.observable(undefined);

        self.isEnabled = ko.pureComputed(function () {
            return self.enabled();
        });
        self.isDisabled = ko.pureComputed(function () {
            return !self.enabled();
        });

        self.setEnabled = function (state) {
            self.enabled(!!state);
            OctoPrint.settings.save({
                plugins: {
                    poweroffafterprint: {
                        enabled: self.enabled()
                    }
                }
            });
        };

        function _updateSelectedState(source, target) {
            target(source() === null ? "Unchanged" : !!source() ? "Enabled" : "Disabled");
        }

        self.onBeforeBinding = function () {
            self._settings = self.settingsView.settings.plugins.poweroffafterprint;
            self._writeSettings(self._settings, self);

            _updateSelectedState(self.stateAfterStartup, self._selectedStateAfterStartup);
            _updateSelectedState(
                self.stateAfterPrintStart,
                self._selectedStateAfterPrintStart
            );
            _updateSelectedState(
                self.stateAfterPrintDone,
                self._selectedStateAfterPrintDone
            );
        };

        self.onSettingsBeforeSave = function () {
            self.stateAfterStartup(self.states[self._selectedStateAfterStartup()]);
            self.stateAfterPrintStart(self.states[self._selectedStateAfterPrintStart()]);
            self.stateAfterPrintDone(self.states[self._selectedStateAfterPrintDone()]);

            self._writeSettings(self, self._settings);
        };

        self._writeSettings = function (source, target) {
            target.powerOffScript(source.powerOffScript());
            target.powerOffOnDone(source.powerOffOnDone());
            target.powerOffOnFail(source.powerOffOnFail());
            target.powerOffOnCancel(source.powerOffOnCancel());
            target.stateAfterStartup(source.stateAfterStartup());
            target.stateAfterPrintStart(source.stateAfterPrintStart());
            target.stateAfterPrintDone(source.stateAfterPrintDone());
            target.enabled(source.enabled());
        };

        self.onDataUpdaterPluginMessage = function (plugin, data) {
            if (plugin != PLUGIN_ID) {
                return;
            }

            if (data.settings) {
                self._writeSettings(ko.mapping.fromJS(data.settings), self);
            }
        };
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: PowerOffAfterPrintViewModel,
        dependencies: ["settingsViewModel"],
        elements: [
            "#sidebar_plugin_poweroffafterprint",
            "#settings_plugin_poweroffafterprint"
        ]
    });
});
