# This will be called by the PHP page to generate the chart data.
# robcranfill
# Simply output the Apache EChart JSON fragment to stdout.


print("            {")
print("              data: [10, 20, 20, 35, 45, 25, 0],")
print("              type: 'bar',")
print("              stack: 'x'")
print("            },")
print("            {")
print("              data: [50, 40, 30, 50, 0, 15, 0],")
print("              type: 'bar',")
print("              stack: 'x'")
print("            },")
print("            {")
print("              data: [10, 20, 30, 40, 0, 0, 0],")
print("              type: 'bar',")
print("              stack: 'x'")
print("            }")

