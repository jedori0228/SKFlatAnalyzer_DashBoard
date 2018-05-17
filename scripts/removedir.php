<?php

if(isset($_POST['ToMove']) && is_array($_POST['ToMove'])){
  foreach ($_POST['ToMove'] as $dir) {
    shell_exec('mv /var/www/html/SKFlatAnalyzerJobLogs/' . $dir . ' /var/www/html/SKFlatAnalyzerJobLogs/Done/');
  };
}
else{
  echo "Not Set<br>";
}

if(isset($_POST['ToRemove']) && is_array($_POST['ToRemove'])){
  foreach ($_POST['ToRemove'] as $dir) {
    shell_exec('rm -rf /var/www/html/SKFlatAnalyzerJobLogs/' . $dir);
  };
}
else{
  echo "Not Set<br>";
}

$output=shell_exec('cd /var/www/html/SKFlatAnalyzerJobLogs/; python make_html.py');
header('Location: http://147.47.242.71/SKFlatAnalyzerJobLogs/JobLogs.html')
?>
