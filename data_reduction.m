% Use file selection dialog to choose the CSV file
[filename, filepath] = uigetfile({'*.csv', 'CSV Files (*.csv)'; '*.*', 'All Files (*.*)'}, 'Select CSV Data File');
if isequal(filename, 0) || isequal(filepath, 0)
    disp('File selection canceled');
    return;
end

% Load file
fullFilePath = fullfile(filepath, filename);
data = readtable(fullFilePath, 'VariableNamingRule', 'preserve');

% Build timestamps using row index * 20 ms (starting at 0 ms)
numSamples = height(data);
timestamps = milliseconds((0:numSamples - 1) * 20);  % Row 1 = 0 ms, Row 2 = 20 ms, ...

% Column identification
varNames = data.Properties.VariableNames;
ptCols = contains(varNames, 'PT-', 'IgnoreCase', true) & contains(varNames, 'Pressure', 'IgnoreCase', true);
stateCols = contains(varNames, 'State', 'IgnoreCase', true);

% Extract data
ptData = data{:, ptCols};
rawStateData = data{:, stateCols};
if iscell(rawStateData)
    if isvector(rawStateData)
        stateData = strcmpi(rawStateData, 'True');
    else
        stateData = cellfun(@(x) strcmpi(x, 'True'), rawStateData);
    end
else
    stateData = rawStateData;
end
stateData = double(stateData);

% Labels
ptLabels = varNames(ptCols);
stateLabels = varNames(stateCols);

% Start plotting
figure;

% ---- Plot PTs on left axis ----
yyaxis left
hold on
colors = lines(size(ptData, 2));  % PT line colors
ptLines = gobjects(1, size(ptData, 2));
for i = 1:size(ptData, 2)
    ptLines(i) = plot(timestamps, ptData(:, i), '-', ...
        'Color', colors(i, :), ...
        'LineWidth', 1.5, ...
        'DisplayName', ptLabels{i});
end
ylabel('Pressure');

% ---- Plot solenoids on right axis ----
yyaxis right
hold on
solenoidColors = parula(size(stateData, 2));  % Solenoid line colors
stateLines = gobjects(1, size(stateData, 2));
for i = 1:size(stateData, 2)
    stateLines(i) = plot(timestamps, stateData(:, i), '--', ...
        'Color', solenoidColors(i, :), ...
        'LineWidth', 1.2, ...
        'DisplayName', stateLabels{i});
end
ylim([-0.1 1.2]);
ylabel('Solenoid/Binary State');

% ---- Interactive data tips for PTs ----
dcm = datacursormode;
dcm.Enable = 'on';
dcm.DisplayStyle = 'datatip';
set(dcm, 'UpdateFcn', @(~, event_obj) ...
 sprintf('%s\nTime: %.2f ms\nValue: %.4f', ...
 get(event_obj.Target, 'DisplayName'), ...
 event_obj.Position(1), ...
 event_obj.Position(2)));

% ---- Unified Legend ----
allLines = [ptLines, stateLines];
legend(allLines, 'Location', 'northeast');

xlabel('Time');
title('Pressure and Solenoid States Over Time');
grid on;

% ---- Auto-save figure using input CSV file name ----
[~, nameWithoutExt, ~] = fileparts(filename);  % Strip .csv extension

% Save as .png
pngFile = fullfile(filepath, [nameWithoutExt, '.png']);
exportgraphics(gcf, pngFile);

% Save as .fig
figFile = fullfile(filepath, [nameWithoutExt, '.fig']);
savefig(gcf, figFile);

disp(['Figure saved as PNG: ', pngFile]);
disp(['Figure saved as FIG: ', figFile]);