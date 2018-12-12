title: A News Verification Browser for the Detection of Clickbait, Satire, and Falsified News

tags:
- clickbait
- satire
- fake news
- misinformation
- disinformation
authors:
- name: Victoria L. Rubin
  orcid: 0000-0003-3610-9967    affiliation: 1
- name: Chris Brogly
  orcid: 0000-0001-5688-0287    affiliation: 1
- name: Nadia Conroy
  orcid: 0000-0003-4826-4489    affiliation: 1
- name: Yimin Chen
  orcid: 0000-0002-0924-3661    affiliation: 1
- name: Sarah E. Cornwell
  orcid: 0000-0002-2367-3668    affiliation: 1
- name: Toluwase V. Asubiaro    
  orcid: 0000-0003-0718-7739affiliation: "1, 2"
affiliations: 
- name: The Language and Information Technology Research Lab (LiT.RL), The Faculty of Media and Information Studies, The University of Western Ontario, London, Ontario, Canada.
  index: 1
- name: E. Latunde Odeku Medical Library, College of Medicine, University of Ibadan, Ibadan, Nigeria
  index: 2 
- name: Media Sonar Technologies, London, Ontario, Canada.
  index: 3
date: 12 December 2018
bibliography: paper.bib

# Description-in-Brief
The LiT.RL News Verification Browser is a research tool for news readers, journalists, editors or information professionals. The tool analyzes the language used in digital news web pages to determine if they are clickbait, satirical news, or falsified news, and visualizes the results by highlighting content in color-coded categories.

# Summary
Widespread adoption of internet technologies has changed the way that news is created and consumed. The current online news environment is one that incentivizes speed and spectacle in reporting at the cost of fact-checking and verification, encouraging the proliferation of misinformation and disinformation. The LiT.RL News Verification (NV) Browser is a system that offers a first step counter-measure by automatically detecting and highlighting fake news headlines and articles. The system is presented to users as a set of assistive technologies built into a stand-alone browser tuned to identify different varieties of fakes [@Rubin:2015; @Rubin:2017]. Our algorithms look for patterns of subtle lexico-syntactic features in text. Images, audio and video formats are unsupported. The core of the functionality is in the natural language processing (NLP) of textual data and automated classification of results with machine learning using support vector machines.

The LiT.RL NV Browser offers three discrete functionalities:
a.	Detection of clickbait headlines [@Chen:2015:MOC:2823465.2823467; @brogly];
b.	Detection of satirical article content [@Rubin:2016];
c.	Detection of falsified news articles [@Rubin:2012; @Asubiaro].

Each is implemented as a separate overlay option through three tabs at the bottom right of the browser. Currently in its proof of concept stage, the system runs over a batch of website content, such as news feed on a website, and visualizes the results by highlighting content in red, orange or green, by analogy with the traffic stop-light.
 
![Figure 1: Screenshot of LiT.RL News Verification Browser clickbait detection on the CNN homepage (December 12, 2018)](figure.png)

# Limitations
This browser is meant to augment our human discernment, rather than replace it, by highlighting potentially false information which may require further scrutiny. Digital literacy is key for everyone to effectively evaluate potential misinformation online, and the LiT.RL Browser is NOT a replacement for that. News readers’ critical thinking remains key to navigating the increasingly fraught online information landscape. The News Verification Browser is not a replacement for a day-to-day web browser and should not be used where security is critical. 

# Availability
 The source code is openly available on GitHub [@litrl2018] under the GPLv3 license for anyone in the research and development community to use or improve on. The public can download the browser for experimentation on their own computers with “no strings attached”. 

# Acknowledgements
This research has been funded by the Government of Canada Social Sciences and Humanities Research Council (SSHRC) Insight Grant (#435-2015-0065) awarded to Dr. Victoria L. Rubin for the 2015-2018 project entitled “Digital Deception Detection: Identifying Deliberate Misinformation in Online News”.

# References
