REM DONT FORGET THIS:
REM Need to download NLTK packages in a script
REM >>> import nltk
REM >>> nltk.download()
REM If you install on a network share, you need to point to your python.exe install... "python" wont be on your PATH environment variable
echo Installing Python 2.7.....
"./dependencies/python-2.7.15.msi" /quiet /norestart
set path=C:\Python27
echo Setting up Python packages needed by NVS...
python -m pip install virtualenv
python -m virtualenv pydeps
".\pydeps\Scripts\python" -m pip install scipy==1.1.0
".\pydeps\Scripts\python" -m pip install numpy==1.15.4
".\pydeps\Scripts\python" -m pip install nltk==3.2.4
".\pydeps\Scripts\python" "dependencies/downloadNLTK.py"
".\pydeps\Scripts\python" -m pip install pattern==2.6
".\pydeps\Scripts\python" -m pip install pandas==0.22.0
".\pydeps\Scripts\python" -m pip install scikit-learn==0.18.2
".\pydeps\Scripts\python" -m pip install json_lines==0.3.1
".\pydeps\Scripts\python" -m pip install xlsxwriter==0.9.8
".\pydeps\Scripts\python" -m pip install html==1.16
".\pydeps\Scripts\python" -m pip install dill==0.2.7.1