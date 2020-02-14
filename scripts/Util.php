<?php

if(isset($_POST['Refresh'])){
  echo "Refresh <br>";
  shell_exec('cd ../; python make_html.py');
  echo "Refresh done<br>";
  header('Location: ../JobLogs.html');
  exit;
}

shell_exec('cd ../; python make_html.py');
header('Location: JobLogs.html');
?>
