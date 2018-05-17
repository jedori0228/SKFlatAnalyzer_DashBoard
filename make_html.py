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
  img {
      display: block;
      margin-left: auto;
      margin-right: auto;
  }

  </style>



  <script type="text/javascript">

    function realtimeClock() {
      document.getElementById('myclock').innerHTML = 'Last updated at '+getTimeStamp()
      //setTimeout("realtimeClock()", 1000);
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

<form action="http://147.47.242.71/SKFlatAnalyzerJobLogs/scripts/removedir.php" method="post">

<p align="center"> <input type="submit" name="Refresh" value="Refresh"> </p>
<p align="center"> <input type="submit" name="SubmitChange" value="Change"> </p>

<table border = 1 align="center">
  <tr>
    <th><a name="LHE Log files">SKFlatAnalyzer Job Logs</a></th>
    <th>Jot Status</th>
    <th>Event Status</th>
    <th>Run Time</th>
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
  line_EstTime=""

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
      line_EstTime = loglines[j].replace('Estimted Finishing Time : ','')
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
  esttime_words = line_EstTime.split()
  esttime_days = esttime_words[0].split('-')
  esttime_times = esttime_words[1].split(':')
  EstTime = datetime.datetime(int(esttime_days[0]),int(esttime_days[1]),int(esttime_days[2]),int(esttime_times[0]),int(esttime_times[1]),int(esttime_times[2]))
  LeftTime = EstTime-Now

  left_inseconds = 86400*LeftTime.days+LeftTime.seconds

  ## find total run time
  line_StartTime = ""
  for i in range(0,nlines):
    if "Job submitted at" in loglines[i]:
      line_StartTime = loglines[i].replace('Job submitted at ','')
      break
  starttime_words = line_StartTime.split()
  starttime_days = starttime_words[0].split('-')
  starttime_times = starttime_words[1].split(':')
  StartTime = datetime.datetime(int(starttime_days[0]),int(starttime_days[1]),int(starttime_days[2]),int(starttime_times[0]),int(starttime_times[1]),int(starttime_times[2]))

  line_LastCheckTime = ""
  for i in range(0,nlines):
    if "Last checked at" in loglines[i]:
      line_LastCheckTime = loglines[i].replace('Last checked at ','')
      break
  lastchecktime_words = line_LastCheckTime.split()
  lastchecktime_days = lastchecktime_words[0].split('-')
  lastchecktime_times = lastchecktime_words[1].split(':')
  LastCheckTime = datetime.datetime(int(lastchecktime_days[0]),int(lastchecktime_days[1]),int(lastchecktime_days[2]),int(lastchecktime_times[0]),int(lastchecktime_times[1]),int(lastchecktime_times[2]))

  TotalRunTime = LastCheckTime-StartTime
  totalrun_days = TotalRunTime.days
  totalrun_seconds = TotalRunTime.seconds
  totalrun_hours = totalrun_seconds/3600
  totalrun_minutes = (totalrun_seconds-3600*totalrun_hours)/60
  totalrun_seconds = totalrun_seconds-3600*totalrun_hours-totalrun_minutes*60
  totalrun_inseconds = 86400*TotalRunTime.days+TotalRunTime.seconds

  ## column : total run time; e.g., *d *h *m *s
  string_totalrun = str(totalrun_days)+'d'+str(totalrun_hours)+'h'+str(totalrun_minutes)+'m'+str(totalrun_seconds)+'s'
  #out.write('    <td align="center">'+string_totalrun+'</td>\n')
  out.write('    <td align="center">'+str(totalrun_inseconds)+' s</td>\n')

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

print>>out,'''</table>

</form>

<br />
<br />
<img src="http://147.47.242.71/Public/SKFlatAnalyzer_DashBoard/tangtang.gif" alt="WorkingVeryHard" align="middle">

</body>

</html>
'''
out.close()

