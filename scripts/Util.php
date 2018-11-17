<?php

if(isset($_POST['GoToSaved'])){
  echo "GoToSaved <br>";
  header('Location: http://147.47.242.71/SKFlatAnalyzerJobLogs/SavedJobLogs/JobLogs.html');
  exit;
}

if(isset($_POST['Refresh'])){
  echo "Refresh <br>";
  shell_exec('cd /var/www/html/SKFlatAnalyzerJobLogs/; python make_html.py');
  echo "Refresh done<br>";
  header('Location: http://147.47.242.71/SKFlatAnalyzerJobLogs/JobLogs.html');
  exit;
}

if(isset($_POST['ToCopy']) && is_array($_POST['ToCopy'])){
  foreach ($_POST['ToCopy'] as $dir) {
    shell_exec('cp -r /var/www/html/SKFlatAnalyzerJobLogs/' . $dir . ' /var/www/html/SKFlatAnalyzerJobLogs/SavedJobLogs/; chmod -R 775 /var/www/html/SKFlatAnalyzerJobLogs/SavedJobLogs/');
  };
}

if(isset($_POST['ToMove']) && is_array($_POST['ToMove'])){
  foreach ($_POST['ToMove'] as $dir) {
    shell_exec('mv /var/www/html/SKFlatAnalyzerJobLogs/' . $dir . ' /var/www/html/SKFlatAnalyzerJobLogs/SavedJobLogs/');
  };
}
else{
  echo "ToMove Not Set <br>";
}

if(isset($_POST['ToRemove']) && is_array($_POST['ToRemove'])){
  #echo "Remove";
  foreach ($_POST['ToRemove'] as $dir) {
    echo "rm -rf /var/www/html/SKFlatAnalyzerJobLogs/" . $dir;
    shell_exec('rm -rf /var/www/html/SKFlatAnalyzerJobLogs/' . $dir);
  };
  #echo "Remove done";
}
else{
  echo "ToRemove Not Set <br>";
}

shell_exec('cd /var/www/html/SKFlatAnalyzerJobLogs/; python make_html.py');
header('Location: http://147.47.242.71/SKFlatAnalyzerJobLogs/JobLogs.html');
?>
