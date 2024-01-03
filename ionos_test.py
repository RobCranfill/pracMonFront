# This will be called by the PHP page to generate the chart data.
# robcranfill

def print_test_data_2():

    print("<p>this is a test.</p><p>how does this look?</p>")


def print_test_data():
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


print_test_data_2()

# # does this work in PHP?
# if __name__ == "__main__":
#     print_test_data()
