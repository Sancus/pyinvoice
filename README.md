# pyinvoice

This command line hour tracker and invoice printer lets you register hours worked and then print a LaTeX invoice template which can be turned into pdf with pdflatex or any other tool.

Setup:
Enter your details into settings.py, following the settings.py.example.

`pip install -r requirements.txt`

Then `python worked.py start -s 2017-04-01'` or whatever date you want to start tracking. I generally rename the `project.json` and start a new one each month.

Edit the `project.json` to add a name and a rate($ currency/hour) to the project.

`python worked.py <number of hours> <comment>` will register number of hours worked, and the -s date argument can be used here too. If no date is specified, the default is *today* based on system local time.

`python worked.py summary` will print a list of hours worked like so:

`Tuesday 2017-03-21 - 7 hours.`  
`Wednesday 2017-03-22 - 9 hours.`  
`Thursday 2017-03-23 - 8 hours.`  
`Friday 2017-03-24 - 2 hours.`  
`Sunday 2017-03-26 - 2 hours.`  
`Monday 2017-03-27 - 7 hours.`  
`Tuesday 2017-03-28 - 8 hours.`  
`Wednesday 2017-03-29 - 4 hours.`  
`Thursday 2017-03-30 - 1 hours.`  
`Friday 2017-03-31 - 8 hours.`  
`Saturday 2017-04-01 - 5 hours.`  
`You've worked 61 hours on project Example since 2017-03-21.`  

It will add up multiple instances for each day, so if you worked 2,3,and 2 hours on a particular day with separate comments, they will be added together in the summary output.

Once you're done tracking hours, you can print an invoice with:
`python invoice.py` and if you want to turn it into pdf, you'll need to install texlive and do:
`python invoice.py | pdflatex`.

Make sure you have the right texlive packages installed, particularly ltablex.
