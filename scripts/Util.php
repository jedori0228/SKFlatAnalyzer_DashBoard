<?php

if(isset($_POST['GoToSaved'])){
  echo "GoToSaved <br>";
  header('Location: ../SavedJobLogs/JobLogs.html');
  exit;
}

if(isset($_POST['Refresh'])){
  echo "Refresh <br>";
  shell_exec('cd ../; python make_html.py');
  echo "Refresh done<br>";
  header('Location: ../JobLogs.html');
  exit;
}

if(isset($_POST['ToCopy']) && is_array($_POST['ToCopy'])){
  foreach ($_POST['ToCopy'] as $dir) {
    shell_exec('cp -r ../' . $dir . ' ../SavedJobLogs/; chmod -R 775 ../SavedJobLogs/');
  };
}

if(isset($_POST['ToMove']) && is_array($_POST['ToMove'])){
  foreach ($_POST['ToMove'] as $dir) {
    shell_exec('mv ../' . $dir . ' ../SavedJobLogs/');
  };
}
else{
  echo "ToMove Not Set <br>";
}

if(isset($_POST['ToRemove']) && is_array($_POST['ToRemove'])){
  #echo "Remove";
  foreach ($_POST['ToRemove'] as $dir) {
    echo "rm -rf ../" . $dir;
    shell_exec('rm -rf ../' . $dir);
  };
  #echo "Remove done";
}
else{
  echo "ToRemove Not Set <br>";
}

shell_exec('cd ../; python make_html.py');
header('Location: JobLogs.html');
?>
