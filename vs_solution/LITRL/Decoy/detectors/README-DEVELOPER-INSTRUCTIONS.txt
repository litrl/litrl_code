The detectors folder should have one subdirectory for each detector in the browser.
Inside the subfolder, include only the nvs<detector_name>.py and any modules it needs.
The browser should be configured to load the detectors from this directory; see the clickbait path in FrmMain.cs for an example.
To add the files, create the directories in the visual studio project by right-clicking. Then, add your relevant python and data files, but use "Add Link".