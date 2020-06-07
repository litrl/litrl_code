REM DONT FORGET THIS:
REM Need to download NLTK packages in a script
REM >>> import nltk
REM >>> nltk.download()
REM If you install on a network share, you need to point to your python.exe install... "python" wont be on your PATH environment variable
echo Installing Python 3.....
"./dependencies/python-3.6.8-amd64.exe" /quiet /norestart InstallAllUsers=1 TargetDir="C:\Python36"
set path=C:\Python36
echo Setting up Python packages needed by NVS...
python -m pip install virtualenv
python -m virtualenv pydeps
".\pydeps\Scripts\python" -m pip install scipy==1.4.1
".\pydeps\Scripts\python" -m pip install numpy==1.18.5
".\pydeps\Scripts\python" -m pip install nltk==3.5
".\pydeps\Scripts\python" "dependencies/downloadNLTK.py"
".\pydeps\Scripts\python" -m pip install pattern==3.6
".\pydeps\Scripts\python" -m pip install pandas==1.0.4
".\pydeps\Scripts\python" -m pip install scikit-learn==0.23.1
".\pydeps\Scripts\python" -m pip install json_lines==0.5.0
".\pydeps\Scripts\python" -m pip install xlsxwriter==1.2.9
REM ".\pydeps\Scripts\python" -m pip install html==1.16
".\pydeps\Scripts\python" -m pip install dill==0.3.1.1