# Litrl Browser

Demonstration: https://www.youtube.com/watch?v=OtitQ-f4AL4

The Litrl (pronouned "literal") Browser is a research tool for news readers, journalists, editors or information professionals. The tool analyzes the language used in digital news web pages to determine if they are clickbait, satirical news, or falsified news. The current online news environment is one that incentivizes speed and spectacle in reporting at the cost of fact-checking and verification, encouraging the proliferation of misinformation and disinformation. The LiT.RL News Verification (NV) Browser is a system that offers a first step counter-measure by automatically detecting and highlighting clickbait (to 94% accuracy on a test set of 5670 texts), satire (to 84% accuracy on a test set of 95 texts), and falsified text (to 71% accuracy on a test set of 28 texts). The browser was built to study the effectiveness of these deception detectors when applied to real-world internet use, where the accuracy of these detectors may vary considerably given the range of text online. Digital literacy is key for everyone to effectively evaluate potential misinformation online, and the Litrl Browser is **NOT** a replacement for that. All processing is completed on the local machine - clickbait, satirical news, and falsified news results are not sent to or from a remote server. Results may be saved locally to a standard SQLite database for further analysis. Please note that Litrl Browser is not perfect and is not always correct. 

The Litrl Browser is based on Prof. Victoria Rubin's (Western University, Canada) News Verification Suite concept (https://www.researchgate.net/publication/316754164_News_Verification_Suite_Towards_System_Design_to_Supplement_Reporters'_and_Editors'_Judgements).

Litrl Browser should be used with caution as it is still highly experimental, may contain bugs and security issues, and was intended to be used as a tool for further research into deception on the internet and the effectiveness of deception detectors. It is **NOT** designed as a replacement for your day-to-day web browser and should not be used where security is critical. The falsifications detector is still in very early stages and is still being written - although it performs acceptably on test data, in practice it is not always effective. Use this feature with added caution.

The software was developed by the LiT.RL (Language and Information Technology Research Lab) at FIMS (Faculty of Information and Media Studies), Western University, Canada.

Litrl Browser is licensed under the GPLv3.

### Questions and inquiries should be directed to:
litrlbrowser@gmail.com

### If you use Litrl Browser for research we ask that you cite the following:
Rubin et al., (2019). A News Verification Browser for the Detection of Clickbait, Satire, and Falsified News. Journal of Open Source Software, 4(35), 1208, https://doi.org/10.21105/joss.01208

[![DOI](http://joss.theoj.org/papers/10.21105/joss.01208/status.svg)](https://doi.org/10.21105/joss.01208)

### The latest archived version of the browser with a DOI can be found here:
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2588566.svg)](https://doi.org/10.5281/zenodo.2588566)

### The initial archived version of the browser with a DOI, released in 2018, can be found here:
Rubin, Victoria L.; Brogly, Chris; Conroy, Nadia; Chen, Yimin; Cornwell, Sarah E.; Asubiaro, Toluwase V. (2018). litrl/litrl_code: Litrl Browser Experimental 0.12.0.0 Public (Version exp-0.12.0.0). Zenodo. 10.5281/zenodo.2016627.

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
1) VC++ 2017 redistributable: https://aka.ms/vs/15/release/vc_redist.x64.exe
2) .NET 4.6.2 (minimum) runtime: https://dotnet.microsoft.com/download/thank-you/net462

Then run the installer for the Litrl Browser. Dependencies are not included.

The installer package for modern Windows systems (7, 8.1, 10) is available under "Releases." The installer takes a few minutes - please be patient! A lot of work is currently done with a batch script - the command prompt may be open for a few minutes - do not close it. The default install location is your desktop, where one folder and one shortcut will be created (other locations are untested).

## Uninstalling the software
Simply delete the Litrl Browser shortcut and LITRL folder from your desktop. That's it!

## Compiling and running the software
Please see the Development & Build process page on the wiki at https://github.com/litrl/litrl_code/wiki/Development-&-build-process

## Acknowledgments
This research has been funded by the Government of Canada Social Sciences and Humanities Research Council 
(SSHRC) Insight Grant (#435-2015-0065) awarded to Dr. Rubin for the project entitled Digital Deception Detection: 
Identifying Deliberate Misinformation in Online News. 

## References

[CLICKBAIT DATASET 1] Abhijnan Chakraborty, Bhargavi Paranjape, Sourya Kakarla, and Niloy Ganguly. "Stop Clickbait: Detecting and Preventing Clickbaits in Online News Media”. In Proceedings of the 2016 IEEE/ACM International Conference on Advances in Social Networks Analysis and Mining (ASONAM), San Fransisco, US, August 2016. (URL: https://github.com/bhargaviparanjape/clickbait)

[CLICKBAIT DATASET 2] Martin Potthast, Tim Gollub, Kristof Komlossy, Sebastian Schuster, Matti Wiegmann, Erika Patricia Garces Fernandez, Matthias Hagen, and Benno Stein. Crowdsourcing a Large Corpus of Clickbait on Twitter. In Proceedings of the 27th International Conference on Computational Linguistics (COLING 2018), pages 1498–1507, August 2018. The COLING 2018 Organizing Committee. (URL: https://webis.de/data/webis-clickbait-17.html)

[SATIRE DATASET 1] Rubin, V. R., Conroy, N. J., Chen, Y. & Cornwell, S. (2016) Fake News or Truth? Using Satirical Cues to Detect Potentially Misleading News. In the Proceedings of the Workshop on Computational Approaches to Deception Detection at the 15th Annual Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies.  (NAACL-CADD2016), San Diego, California, June 17, 2016.

Library licenses can be found in the "licenses" folder.
