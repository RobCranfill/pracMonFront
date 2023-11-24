<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Practice Monitor</title>
    <!-- Include the ECharts file you just downloaded -->
    <script src="echarts.js"></script>
  </head>
  <body>
    <!-- Prepare a DOM with a defined width and height for ECharts -->
    <div id="main" style="width: 600px;height:400px;"></div>
    <script type="text/javascript">
      // Initialize the echarts instance based on the prepared dom
      var myChart = echarts.init(document.getElementById('main'));

      // Specify the configuration items and data for the chart
      var option = {
        title: {
          text: 'Practice Monitor - Sept 23-29'
        },
        tooltip: {},
        xAxis: {
          data: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        },
        yAxis: {},
        series: [

          <?php
          passthru('/usr/bin/python3 ./out1.py');
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