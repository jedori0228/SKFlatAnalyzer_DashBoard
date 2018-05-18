<?php

if(isset($_POST['GoToRunning'])){
  echo "GoToRunning <br>";
  header('Location: http://147.47.242.71/SKFlatAnalyzerJobLogs/JobLogs.html');
  exit;
}

if(isset($_POST['Refresh'])){
  echo "Refresh <br>";
  shell_exec('cd /var/www/html/SKFlatAnalyzerJobLogs/SavedJobLogs/; python make_SavedJobLogs_html.py');
  echo "Refresh done<br>";
}

if(isset($_POST['ToRemove']) && is_array($_POST['ToRemove'])){
  foreach ($_POST['ToRemove'] as $dir) {
    shell_exec('rm -rf /var/www/html/SKFlatAnalyzerJobLogs/SavedJobLogs/' . $dir);
  };
}
else{
  echo "ToRemove Not Set <br>";
}

header('Location: http://147.47.242.71/SKFlatAnalyzerJobLogs/SavedJobLogs/JobLogs.html');
?>
