# Litrl Browser

Demonstration: https://www.youtube.com/watch?v=OtitQ-f4AL4

Welcome to the Litrl (pronounced "literal") Browser, which implements aspects of Prof. Victoria Rubin's (Western University, Canada) News Verification Suite concept (https://www.researchgate.net/publication/316754164_News_Verification_Suite_Towards_System_Design_to_Supplement_Reporters'_and_Editors'_Judgements)

The Litrl Browser provides visual identification of clickbait, satire, and falsification text, to a certain accuracy level. Images and video are unsupported - only text is processed. Litrl Browser is not perfect and is not always correct. Digital literacy is key for everyone to effectively evaluate potential misinformation online, and the Litrl Browser is **NOT** a replacement for that.

Litrl Browser is still highly experimental, may contain bugs and security issues, and was intended to be used as a tool for further research into deception on the internet and the effectiveness of deception detectors. It is **NOT** designed as a replacement for your day-to-day web browser and should not be used where security is critical. The falsifications detector is still in very early alpha stages and is still being written - although it performs acceptably on test data, in practice it is not always effective. Use this feature with caution.

The software was developed by the LiT.RL (Language and Information Technology Research Lab) at FIMS (Faculty of Information and Media Studies), Western University, Canada.

Litrl Browser is licensed under the GPLv3.

### Questions and inquiries should be directed to:
litrlbrowser@gmail.com

### If you use Litrl Browser for research, we ask that you cite the following for now (a full publication is in process):
Rubin, Victoria L., Brogly, Chris, Conroy, Nadia, Chen, Yimin, Cornwell, Sarah, Asubiaro, Toluwase (2018). LitRL News Verification Browser: Clickbait, Satirical Fakes, and Falsified News Detectors. GitHub. https://github.com/litrl/litrl_code. DOI.

[![DOI](https://zenodo.org/badge/160725581.svg)](https://zenodo.org/badge/latestdoi/160725581)

## Why not a plugin?
Various plugins have already been attempted in this area. We decided to develop a separate research tool for deception with a simple user interface that allowed for easier real-world testing of our group's previous work.

## System Requirements
- Windows 7, 8.1 (untested), or 10.
- 1280x720 (720p) minimum screen resolution.
- 1920x1080 (1080p) recommended screen resolution.
- 4:3 (Square) monitors may work but are not supported.
- Relatively modern quad-core 64-bit CPU.
- 4GB of RAM.

## Installing the software
Prerequisites to install:
1) VS 2017 redistributable: https://aka.ms/vs/15/release/vc_redist.x64.exe
2) .NET 4.6.2 (minimum) runtime: https://www.microsoft.com/net/download/dotnet-framework/net462

Then run the installer for the Litrl Browser. Dependencies are not included.

The installer package for modern Windows systems (7, 8.1, 10) is available under "Releases." The installer takes a few minutes - please be patient! A lot of work is currently done with a batch script - the command prompt may be open for a few minutes - do not close it. The default install location is your desktop, where one folder and one shortcut will be created (other locations are untested).

## Uninstalling the software
Simply delete the Litrl Browser shortcut and LITRL folder from your desktop. That's it!

## Acknowledgments
This research has been funded by the Government of Canada Social Sciences and Humanities Research Council 
(SSHRC) Insight Grant (#435-2015-0065) awarded to Dr. Rubin for the project entitled Digital Deception Detection: 
Identifying Deliberate Misinformation in Online News. 

## References

[CLICKBAIT DATASET 1] Abhijnan Chakraborty, Bhargavi Paranjape, Sourya Kakarla, and Niloy Ganguly. "Stop Clickbait: Detecting and Preventing Clickbaits in Online News Media”. In Proceedings of the 2016 IEEE/ACM International Conference on Advances in Social Networks Analysis and Mining (ASONAM), San Fransisco, US, August 2016. (URL: https://github.com/bhargaviparanjape/clickbait)

[CLICKBAIT DATASET 2] Martin Potthast, Tim Gollub, Kristof Komlossy, Sebastian Schuster, Matti Wiegmann, Erika Patricia Garces Fernandez, Matthias Hagen, and Benno Stein. Crowdsourcing a Large Corpus of Clickbait on Twitter. In Proceedings of the 27th International Conference on Computational Linguistics (COLING 2018), pages 1498–1507, August 2018. The COLING 2018 Organizing Committee. (URL: https://webis.de/data/webis-clickbait-17.html)

Library licenses can be found in the "licenses" folder.