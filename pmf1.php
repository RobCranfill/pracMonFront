<!DOCTYPE html>
<html>

  <head>
    <meta charset="utf-8" />
    <title>Practice Monitor</title>

    <!-- load Apache ECharts -->
    <script src="echarts.js"></script>

  </head>

  <body>


<?php

// in mm/dd/yyyy format
$start = $_GET['start'];
if ($start == null) {
  $start = '2023-10-09';
  }

?>

    <!-- Prepare a DOM with a defined width and height for ECharts -->
    <div id="main" style="width: 600px;height:400px;"></div>

    <script type="text/javascript">
      
      // Initialize the echarts instance based on the prepared dom
      var myChart = echarts.init(document.getElementById('main'));

      // Specify the configuration items and data for the chart
      var option = {
        title: {
          text: 'Practice Monitor - Week of <?= $start ?>'
        },
        tooltip: {},
        xAxis: {
          data: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        },
        yAxis: {},
        series: [

          <?php
      
          // calling php - was /usr/bin/python3
          // echo "// start is $start\n";

          passthru("python3 ./get_session_data.py `cat ./aio_secret.text` test-data-1 $start");
          ?>
        ]
      };

      // Display the chart using the configuration items and data just specified.
      myChart.setOption(option);
    </script>

<br>
<?php phpinfo(); ?>

  </body>
</html>