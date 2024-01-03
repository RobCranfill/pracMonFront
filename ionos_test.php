<!DOCTYPE html>
<html>

  <head>
    <meta charset="utf-8" />
    <title>Ionos PHP test</title>
  </head>

  <body>

<?php echo '<p>Hello Cran!</p>'; ?>

<?php
passthru('python3 ./ionos_test.py this_is_a_test');
?>


<br>
<br>
<br>
<br>
<br>
<br>
<br>

<?php phpinfo(); ?>


  </body>
</html>