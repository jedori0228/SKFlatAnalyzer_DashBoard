import os
import datetime

forbidden_dir = [
"auth", "Done", "scripts", "backup", "images"
]

Now = datetime.datetime.now()
NowStamp =  Now.strftime('%Y/%m/%d %H:%M:%S')

os.system("ls -d */ | cut -f1 -d'/' > dirlist.txt")
jobdirs = open('dirlist.txt').readlines()

out = open('JobLogs.html','w')

print>>out,'''<!DOCTYPE html>
<html>
<head>

  <style>
  td.Monaco_running{
    font-family: monaco, Consolas, Lucida Console, monospace;
    text-align: center;
  }
  td.Monaco_finished{
    font-family: monaco, Consolas, Lucida Console, monospace;
    text-align: center;
    color: #00cc66;
  }
  p.Clock{
    text-align: center;
    font-size: 30px;
  }
  </style>



  <script type="text/javascript">

    function realtimeClock() {
      document.getElementById('myclock').innerHTML = getTimeStamp()
      setTimeout("realtimeClock()", 1000);
    }


    function getTimeStamp() {
      var d = new Date();

      var s =
        leadingZeros(d.getFullYear(), 4) + '-' +
        leadingZeros(d.getMonth() + 1, 2) + '-' +
        leadingZeros(d.getDate(), 2) + ' ' +

        leadingZeros(d.getHours(), 2) + ':' +
        leadingZeros(d.getMinutes(), 2) + ':' +
        leadingZeros(d.getSeconds(), 2);

      return s;
    }


    function leadingZeros(n, digits) {
      var zero = '';
      n = n.toString();

      if (n.length < digits) {
        for (i = 0; i < digits - n.length; i++)
          zero += '0';
      }
      return zero + n;
    }

  </script>

</head>
<body onload="realtimeClock()">

<p id="myclock" class="Clock"> <p>

<form action="scripts/removedir.php" method="post">

<p align="center"> <input type="submit" name="SubmitChange" value="Change"> </p>

<table border = 1 align="center">
  <tr>
    <th><a name="LHE Log files">SKFlatAnalyzer Job Logs</a></th>
    <th>Jot Status</th>
    <th>Event Status</th>
    <th>Est. Time Left</th>
    <th>Move?</th>
    <th>Remove?</th>
  </tr>
'''

for jobdir in jobdirs:

  skipthis = False
  for f in forbidden_dir:
    if f in jobdir:
      skipthis = True
      break
  if skipthis:
    continue

  jobdir = jobdir.strip('\n')

  out.write('  <tr>\n')

  loglines = open(jobdir+'/JobStatus.log').readlines()
  nlines = len(loglines)

  n_running = 0
  n_finished = 0
  event_done = 0
  event_total = 0
  EstTime=""

  nfound=0
  for i in range(0,nlines):

    if nfound==5:
      break

    j = nlines-i-1

    if "jobs are running" in loglines[j]:
      n_running = int(loglines[j].replace(' jobs are running',''))
      nfound += 1
    if "jobs are finished" in loglines[j]:
      n_finished = int(loglines[j].replace(' jobs are finished',''))
      nfound += 1
    if "EventDone" in loglines[j]:
      event_done = int(loglines[j].split()[2])
      nfound += 1
    if "EventTotal" in loglines[j]:
      event_total = int(loglines[j].split()[2])
      nfound += 1
    if "Estimted Finishing Time" in loglines[j]:
      EstTime = loglines[j].replace('Estimted Finishing Time : ','')
      nfound += 1

  n_total = n_running+n_finished

  ## Determine font
  IsAllDone = n_running==0
  string_class = "Monaco_running"
  if IsAllDone:
    string_class = "Monaco_finished"

  ## column : link to logfile
  out.write('    <td><a href="'+jobdir+'/JobStatus.log">'+jobdir+'</td>\n')
  ## column : Jot stats; e.g., 40/50
  out.write('    <td class="'+string_class+'">'+str(n_finished)+'/'+str(n_total)+'</td>\n')

  ## make bar status
  bar_percentage = "["
  if event_total==0:
    event_done = 0
    event_total = 1
  for i in range(1,21):
    if i<= 20.*event_done/event_total:
      bar_percentage += "#"
    else:
      bar_percentage += "-"
  bar_percentage += "]"
  number_percentage = round(100.*event_done/event_total,1)
  str_percentage = str( number_percentage )
  if number_percentage<100:
    str_percentage = "&nbsp;"+str_percentage
  if number_percentage<10:
    str_percentage = "&nbsp;"+str_percentage

  ## column : Event status; e.g., [################----] 84.4 %
  out.write('    <td class="'+string_class+'">'+bar_percentage+'\t'+str_percentage+' %&nbsp;</td>\n')


  ## calculate est time
  esttime_words = EstTime.split()
  days = esttime_words[0].split('-')
  times = esttime_words[1].split(':')
  FinishingTime = datetime.datetime(int(days[0]),int(days[1]),int(days[2]),int(times[0]),int(times[1]),int(times[2]))
  LeftTime = FinishingTime-Now

  left_days = LeftTime.days
  left_seconds = LeftTime.seconds
  left_hours = left_seconds/3600
  left_minutes = (left_seconds-3600*left_hours)/60
  left_seconds = left_seconds-3600*left_hours-left_minutes*60

  left_inseconds = 86400*LeftTime.days+LeftTime.seconds

  ## column : est. time; e.g., 254 s
  if IsAllDone:
    out.write('    <td align="center"></td>\n')
  else:
    out.write('    <td align="center">'+str(left_inseconds)+' s</td>\n')

  ## column : ToMove checkbox
  out.write('    <td align="center"><input type="checkbox" name="ToMove[]" value="'+jobdir+'"></td>\n')
  ## column : ToRemove checkbox
  out.write('    <td align="center"><input type="checkbox" name="ToRemove[]" value="'+jobdir+'"></td>\n')

  out.write('  </tr>\n')

print>>out,'''</body>

</html>
'''
out.close()

