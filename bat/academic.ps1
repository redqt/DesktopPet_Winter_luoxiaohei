# PowerShell
& 'D:\miniconda3\Scripts\activate.bat'
conda activate chatglm3
Set-Location -Path E:
Set-Location -Path 'E:\academic\gpt_academic\'
Start-Process -NoNewWindow -FilePath "cmd" -ArgumentList '/k', 'title 11 & python main.py'