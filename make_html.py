import os
import datetime

forbidden_dir = [
"auth", "SavedJobLogs", "scripts", "backup", "etc"
]

Now = datetime.datetime.now()
NowStamp =  Now.strftime('%Y/%m/%d %H:%M:%S')

os.system("ls -d */ | cut -f1 -d'/' > dirlist.txt")
os.system('chmod 775 dirlist.txt')
jobdirs = open('dirlist.txt').readlines()

out = open('JobLogs.html','w')

print>>out,'''<!DOCTYPE html>
<html>
<head>

  <title>Dashboard</title>

  <style>
  p.Title{
    text-align: center;
    font-size: 40px;
  }
  p.Clock{
    text-align: center;
    font-size: 30px;
  }
  td.Monaco_running{
    font-family: monaco, Consolas, Lucida Console, monospace;
    text-align: center;
  }
  td.Monaco_finished{
    font-family: monaco, Consolas, Lucida Console, monospace;
    text-align: center;
    color: #00cc66;
  }
  td.Monaco_TotalEvent{
    font-family: monaco, Consolas, Lucida Console, monospace;
    text-align: right;
  }

  @-webkit-keyframes blink
  {
    0%     { visibility: hidden }
    50%    { visibility: hidden }
    50.01% { visibility: visible }
    100%   { visibility: visible }
  }

  td.Monaco_TotalEvent_Updating{
    -webkit-animation: blink 0.5s infinite linear alternate;
    font-family: monaco, Consolas, Lucida Console, monospace;
    text-align: right;
    color: red;
  }
  td.Monaco_TotalEvent_AllDone{
    font-family: monaco, Consolas, Lucida Console, monospace;
    text-align: center;
    color: green;
  }
  img {
      display: block;
      margin-left: auto;
      margin-right: auto;
  }

  </style>



  <script type="text/javascript">

    function realtimeClock() {
      document.getElementById('myclock').innerHTML = 'Current time : '+getTimeStamp()
      setTimeout("realtimeClock()", 1000);
    }

    function SetClockAndTimeStamp() {
      document.getElementById('TimeStamp').innerHTML = 'Last updated time : '+getTimeStamp()
      realtimeClock()
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
<body onload="SetClockAndTimeStamp()">

<p class="Title"> Dashboard </p>
<!--<p id="myclock" class="Clock"> </p>-->
<p id="TimeStamp" class="Clock"> </p>

<form action="scripts/Util.php" method="post">

<p align="center">
  <input type="submit" name="GoToSaved" value="Go to Saved"> 
  <input type="submit" name="Refresh" value="Refresh"> 
  <input type="submit" name="SubmitChange" value="Submit Change">
</p>

<table border = 1 align="center">
  <tr>
    <th rowspan="2"><a name="LHE Log files">SKFlatAnalyzer Job Logs</a></th>
    <th colspan="3">Job Status</th>
    <th colspan="3">Event</th>
    <th rowspan="2">Time</th>
    <th rowspan="2">Copy?</th>
    <th rowspan="2">Move?</th>
    <th rowspan="2">Remove?</th>
  </tr>
    <th>R</th>
    <th>F</th>
    <th>S</th>
    <th>Total</th>
    <th>Finished</th>
    <th>%</th>
  <tr>
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

  n_totaljob = 0
  n_running = 0
  n_finished = 0
  event_done = 0
  event_total = 0
  maxtimeconsume = 0
  line_EstTime=""

  nfound=0
  for i in range(0,nlines):

    if nfound==7:
      break

    j = nlines-i-1

    if "jobs submitted" in loglines[j]:
      n_totaljob = int(loglines[j].replace(' jobs submitted',''))
      nfound += 1
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
    if "Estimated Finishing Time" in loglines[j]:
      line_EstTime = loglines[j].replace('Estimated Finishing Time : ','')
      nfound += 1
    if "MaxEventRunTime" in loglines[j]:
      maxtimeconsume = int(loglines[j].split()[2])

  ## Determine font
  IsAllDone = n_finished==n_totaljob
  string_class = "Monaco_running"
  if IsAllDone:
    string_class = "Monaco_finished"

  ## column : link to logfile
  out.write('    <td><a href="'+jobdir+'/JobStatus.log">'+jobdir+'</td>\n')
  ## column : Jot stats; e.g., 40/50
  colored_running = '<font color=orange>'+str(n_running)+'</font>'
  colored_finished = '<font color=green>'+str(n_finished)+'</font>'
  colored_totaljob = '<font color=black>'+str(n_totaljob)+'</font>'
  out.write('    <td align="center">'+colored_running+'</td>\n')
  out.write('    <td align="center">'+colored_finished+'</td>\n')
  out.write('    <td align="center">'+colored_totaljob+'</td>\n')

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

  ## x : Event status; e.g., [################----] 84.4 %
  #out.write('    <td class="'+string_class+'">'+bar_percentage+'\t'+str_percentage+' %&nbsp;</td>\n')


  ## column : total event
  if IsAllDone:
    out.write('    <td colspan="2" class="Monaco_TotalEvent_AllDone">'+format(event_total,',d')+'</td>\n')
    out.write('    <td class="Monaco_TotalEvent_AllDone">'+str_percentage+'</td>\n')
  else:
    ## All job started event, so event_total is correct
    if n_running+n_finished != n_totaljob:
      print "--> Updadting"
      out.write('    <td class="Monaco_TotalEvent_Updating">'+format(event_total,',d')+'</td>\n')
      out.write('    <td class="Monaco_TotalEvent_Updating">'+format(event_done,',d')+'</td>\n')
      out.write('    <td class="Monaco_TotalEvent_Updating">'+str_percentage+'</td>\n')
      #out.write('    <td class="Monaco_TotalEvent_Updating">'+bar_percentage+'\t'+str_percentage+' %&nbsp;</td>\n')
    else:
      print "--> Not updating"
      out.write('    <td class="Monaco_TotalEvent">'+format(event_total,',d')+'</td>\n')
      out.write('    <td class="Monaco_TotalEvent">'+format(event_done,',d')+'</td>\n')
      out.write('    <td class="Monaco_TotalEvent">'+str_percentage+'</td>\n')
      #out.write('    <td class="'+string_class+'">'+bar_percentage+'\t'+str_percentage+' %&nbsp;</td>\n')

  ## calculate est time
  esttime_words = line_EstTime.split()
  esttime_days = esttime_words[0].split('-')
  esttime_times = esttime_words[1].split(':')
  EstTime = datetime.datetime(int(esttime_days[0]),int(esttime_days[1]),int(esttime_days[2]),int(esttime_times[0]),int(esttime_times[1]),int(esttime_times[2]))
  LeftTime = EstTime-Now

  left_inseconds = 86400*LeftTime.days+LeftTime.seconds

  ## find total run time
  line_TotalEventRunTime = ""
  for i in range(0,nlines):
    if "TotalEventRunTime" in loglines[i]:
      line_TotalEventRunTime = loglines[i].replace('TotalEventRunTime = ','')
      break
  TotalEventRunTime=0
  if line_TotalEventRunTime is not "":
    TotalEventRunTime = int(line_TotalEventRunTime)

  ## column : est. time; e.g., 254 s
  if IsAllDone:
    out.write('    <td align="center">'+str(TotalEventRunTime)+' (Job max consume = '+str(maxtimeconsume)+')</td>\n')
  else:
    out.write('    <td align="center">'+str(left_inseconds)+' s</td>\n')

  ## column : ToMove checkbox
  out.write('    <td align="center"><input type="checkbox" name="ToCopy[]" value="'+jobdir+'"></td>\n')
  ## column : ToMove checkbox
  out.write('    <td align="center"><input type="checkbox" name="ToMove[]" value="'+jobdir+'"></td>\n')
  ## column : ToRemove checkbox
  out.write('    <td align="center"><input type="checkbox" name="ToRemove[]" value="'+jobdir+'"></td>\n')

  out.write('  </tr>\n')

print>>out,'''</table>

</form>

<br />
<br />
<img src="etc/tangtang.gif" alt="WorkingVeryHard" align="middle">

</body>

</html>
'''
out.close()

