:: Installing required libraries
pip install --upgrade -r requirements


@echo off
echo Finished installing libraries
echo If you haven't download FFmpeg, follow this tutorial to obtain it:
echo https://github.com/adaptlearning/adapt_authoring/wiki/Installing-FFmpeg

choice /C Y /M "Do you want to close the batch file?"
goto Yes

:Yes
echo Closing the batch file...
goto End

:End
