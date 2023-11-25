<!DOCTYPE html>
<html>

  <head>
    <meta charset="utf-8" />
    <title>Practice Monitor</title>

    <!-- load Apache ECharts -->
    <script src="echarts.js"></script>

  </head>

  <body>

    <!-- Prepare a DOM with a defined width and height for ECharts -->
    <div id="main" style="width: 600px;height:400px;"></div>

    <script type="text/javascript">
      
      // Initialize the echarts instance based on the prepared dom
      var myChart = echarts.init(document.getElementById('main'));

      <?php

      // in mm/dd/yyyy format
      $start = $_GET['start'];
      if ($start == null) {
        $start = '11/01/2023';
        }
      ?>

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

          // invoke our Python code to retrieve the IOT data!
          <?php

            // in yy/mm/dd format
            $start = $_GET['start'];
            if ($start == null) {
              $start = '11/01/2023';
            }
      
          passthru('/usr/bin/python3 ./get_session_data.py `cat aio_secret.text` $start');
          ?>
        ]
      };

      // Display the chart using the configuration items and data just specified.
      myChart.setOption(option);
    </script>


<?php echo '<p>Hello Cran!</p>'; ?>
<?php phpinfo(); ?>

  </body>
</html>