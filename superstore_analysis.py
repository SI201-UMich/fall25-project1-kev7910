"""
Name: Kevin Nguyen
Student ID: [Your ID Here]
Email: [Your Email Here]
Collaborators: Claude (GenAI tool) - Used for code structure and function implementation

Function Authors:
- load_csv(): Created with assistance from Claude
- calculate_average(): Created with assistance from Claude
- calculate_profit_margin_by_region(): Created with assistance from Claude
- analyze_discount_impact(): Created with assistance from Claude
- write_results_to_file(): Created with assistance from Claude
- main(): Created with assistance from Claude

Dataset: Sample Superstore
Calculations:
1. Regional Profitability Analysis - Calculate average profit margin by region (uses Region, Sales, Profit)
2. Discount Impact Analysis - Analyze profit differences with/without discounts by category (uses Category, Discount, Profit)
"""

import csv


def load_csv(csv_file):
    """
    Reads a CSV file and transforms it into a list of dictionaries.

    Parameters:
        csv_file (str): Path to the CSV file

    Returns:
        list: List of dictionaries where each dictionary represents a row
    """
    data = []
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            row['Sales'] = float(row['Sales'])
            row['Quantity'] = int(row['Quantity'])
            row['Discount'] = float(row['Discount'])
            row['Profit'] = float(row['Profit'])
            data.append(row)
    return data


def calculate_average(values):
    """
    Helper function to calculate the average of a list of numbers.

    Parameters:
        values (list): List of numeric values

    Returns:
        float: The average of the values, or 0 if list is empty
    """
    if len(values) == 0:
        return 0
    return sum(values) / len(values)


def calculate_profit_margin_by_region(data):
    """
    Calculates the average profit margin (Profit/Sales) for each region.

    Parameters:
        data (list): List of dictionaries containing superstore data

    Returns:
        dict: Dictionary with regions as keys and average profit margins as values
    """
    region_margins = {}

    for row in data:
        region = row['Region']
        sales = row['Sales']
        profit = row['Profit']

        if sales == 0:
            continue

        profit_margin = (profit / sales) * 100

        if region not in region_margins:
            region_margins[region] = []
        region_margins[region].append(profit_margin)

    avg_margins = {}
    for region, margins in region_margins.items():
        avg_margins[region] = calculate_average(margins)

    return avg_margins


def analyze_discount_impact(data):
    """
    Analyzes how discounts affect profit for each product category.
    Compares average profit for orders with discounts vs without discounts.

    Parameters:
        data (list): List of dictionaries containing superstore data

    Returns:
        dict: Nested dictionary with categories and their profit stats
              Format: {'Category': {'with_discount': avg, 'without_discount': avg}}
    """
    category_analysis = {}

    for row in data:
        category = row['Category']
        discount = row['Discount']
        profit = row['Profit']

        if category not in category_analysis:
            category_analysis[category] = {
                'with_discount': [],
                'without_discount': []
            }

        if discount > 0:
            category_analysis[category]['with_discount'].append(profit)
        else:
            category_analysis[category]['without_discount'].append(profit)

    results = {}
    for category, discount_data in category_analysis.items():
        results[category] = {
            'with_discount': calculate_average(discount_data['with_discount']),
            'without_discount': calculate_average(discount_data['without_discount']),
            'count_with_discount': len(discount_data['with_discount']),
            'count_without_discount': len(discount_data['without_discount'])
        }

    return results


def write_results_to_file(regional_data, discount_data, filename):
    """
    Writes analysis results to a CSV file.

    Parameters:
        regional_data (dict): Dictionary of regional profit margins
        discount_data (dict): Dictionary of discount impact analysis
        filename (str): Name of output file

    Returns:
        None (creates a file)
    """
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(['Analysis Results for Sample Superstore Dataset'])
        writer.writerow([])

        writer.writerow(['Regional Profitability Analysis'])
        writer.writerow(['Region', 'Average Profit Margin (%)'])

        for region in sorted(regional_data.keys()):
            margin = regional_data[region]
            writer.writerow([region, f'{margin:.2f}'])

        writer.writerow([])
        writer.writerow([])

        writer.writerow(['Discount Impact Analysis by Category'])
        writer.writerow(['Category', 'Avg Profit (With Discount)', 'Count (With Discount)',
                        'Avg Profit (Without Discount)', 'Count (Without Discount)', 'Difference'])

        for category in sorted(discount_data.keys()):
            data = discount_data[category]
            difference = data['without_discount'] - data['with_discount']
            writer.writerow([
                category,
                f'${data["with_discount"]:.2f}',
                data['count_with_discount'],
                f'${data["without_discount"]:.2f}',
                data['count_without_discount'],
                f'${difference:.2f}'
            ])


def test_calculate_average():
    """
    Test cases for calculate_average function.
    """
    print("Testing calculate_average()...")

    assert abs(calculate_average([10, 20, 30]) - 20.0) < 0.01, "Test 1 Failed"
    print("  Test 1 Passed: Average of [10, 20, 30] = 20.0")

    assert abs(calculate_average([100, -50, 50]) - 33.33) < 0.01, "Test 2 Failed"
    print("  Test 2 Passed: Average of [100, -50, 50] ≈ 33.33")

    assert calculate_average([]) == 0, "Test 3 Failed"
    print("  Test 3 Passed: Average of empty list = 0")

    assert calculate_average([42]) == 42, "Test 4 Failed"
    print("  Test 4 Passed: Average of [42] = 42")

    print("All calculate_average() tests passed!\n")


def test_load_csv():
    """
    Test cases for load_csv function.
    """
    print("Testing load_csv()...")

    data = load_csv('SampleSuperstore.csv')
    assert len(data) > 0, "Test 1 Failed: No data loaded"
    print(f"  Test 1 Passed: Loaded {len(data)} rows")

    first_row = data[0]
    assert isinstance(first_row['Sales'], float), "Test 2 Failed: Sales not float"
    assert isinstance(first_row['Profit'], float), "Test 2 Failed: Profit not float"
    assert isinstance(first_row['Quantity'], int), "Test 2 Failed: Quantity not int"
    print("  Test 2 Passed: Data types correctly converted")

    required_cols = ['Region', 'Sales', 'Profit', 'Category', 'Discount']
    assert all(col in first_row for col in required_cols), "Test 3 Failed: Missing columns"
    print("  Test 3 Passed: All required columns present")

    sales_values = [row['Sales'] for row in data[:100]]
    assert all(isinstance(s, float) for s in sales_values), "Test 4 Failed: Invalid sales values"
    print("  Test 4 Passed: Numeric values properly formatted")

    print("All load_csv() tests passed!\n")


def test_calculate_profit_margin_by_region():
    """
    Test cases for calculate_profit_margin_by_region function.
    """
    print("Testing calculate_profit_margin_by_region()...")

    test_data = [
        {'Region': 'West', 'Sales': 100.0, 'Profit': 10.0},
        {'Region': 'West', 'Sales': 200.0, 'Profit': 20.0},
        {'Region': 'East', 'Sales': 100.0, 'Profit': 5.0}
    ]
    result = calculate_profit_margin_by_region(test_data)
    assert 'West' in result and 'East' in result, "Test 1 Failed: Missing regions"
    assert abs(result['West'] - 10.0) < 0.01, "Test 1 Failed: West margin incorrect"
    print("  Test 1 Passed: Basic profit margin calculation works")

    full_data = load_csv('SampleSuperstore.csv')
    result = calculate_profit_margin_by_region(full_data)
    assert len(result) == 4, "Test 2 Failed: Should have 4 regions"
    print(f"  Test 2 Passed: Found {len(result)} regions in dataset")

    test_data_zero = [
        {'Region': 'North', 'Sales': 0.0, 'Profit': 10.0},
        {'Region': 'North', 'Sales': 100.0, 'Profit': 10.0}
    ]
    result = calculate_profit_margin_by_region(test_data_zero)
    assert abs(result['North'] - 10.0) < 0.01, "Test 3 Failed: Zero sales not handled"
    print("  Test 3 Passed: Zero sales entries handled correctly")

    test_data_loss = [
        {'Region': 'South', 'Sales': 100.0, 'Profit': -20.0}
    ]
    result = calculate_profit_margin_by_region(test_data_loss)
    assert result['South'] < 0, "Test 4 Failed: Negative margin not calculated"
    print("  Test 4 Passed: Negative profit margins calculated correctly")

    print("All calculate_profit_margin_by_region() tests passed!\n")


def test_analyze_discount_impact():
    """
    Test cases for analyze_discount_impact function.
    """
    print("Testing analyze_discount_impact()...")

    test_data = [
        {'Category': 'Furniture', 'Discount': 0.0, 'Profit': 100.0},
        {'Category': 'Furniture', 'Discount': 0.2, 'Profit': 50.0},
        {'Category': 'Technology', 'Discount': 0.0, 'Profit': 200.0}
    ]
    result = analyze_discount_impact(test_data)
    assert 'Furniture' in result, "Test 1 Failed: Furniture category missing"
    assert result['Furniture']['without_discount'] == 100.0, "Test 1 Failed: Without discount incorrect"
    print("  Test 1 Passed: Basic discount analysis works")

    full_data = load_csv('SampleSuperstore.csv')
    result = analyze_discount_impact(full_data)
    assert len(result) == 3, "Test 2 Failed: Should have 3 categories"
    print(f"  Test 2 Passed: Found {len(result)} categories")

    test_data_all_discount = [
        {'Category': 'Office', 'Discount': 0.1, 'Profit': 10.0},
        {'Category': 'Office', 'Discount': 0.2, 'Profit': 20.0}
    ]
    result = analyze_discount_impact(test_data_all_discount)
    assert result['Office']['without_discount'] == 0, "Test 3 Failed: No items without discount"
    assert result['Office']['count_without_discount'] == 0, "Test 3 Failed: Count should be 0"
    print("  Test 3 Passed: Handles cases with all discounted items")

    test_data_negative = [
        {'Category': 'Supplies', 'Discount': 0.5, 'Profit': -100.0},
        {'Category': 'Supplies', 'Discount': 0.0, 'Profit': 50.0}
    ]
    result = analyze_discount_impact(test_data_negative)
    assert result['Supplies']['with_discount'] == -100.0, "Test 4 Failed: Negative profit not handled"
    print("  Test 4 Passed: Negative profits handled correctly")

    print("All analyze_discount_impact() tests passed!\n")


def main():
    """
    Main function that orchestrates the entire analysis workflow.
    """
    print("=" * 60)
    print("Superstore Data Analysis")
    print("=" * 60)
    print()

    print("Running tests...")
    print()
    test_calculate_average()
    test_load_csv()
    test_calculate_profit_margin_by_region()
    test_analyze_discount_impact()

    print("=" * 60)
    print("All tests passed! Now running analysis...")
    print("=" * 60)
    print()

    print("Loading data from SampleSuperstore.csv...")
    data = load_csv('SampleSuperstore.csv')
    print(f"Successfully loaded {len(data)} records")
    print()

    print("Calculating regional profit margins...")
    regional_margins = calculate_profit_margin_by_region(data)
    print("Regional analysis complete!")
    print()

    print("Analyzing discount impact on profitability...")
    discount_analysis = analyze_discount_impact(data)
    print("Discount analysis complete!")
    print()

    output_file = 'analysis_results.csv'
    print(f"Writing results to {output_file}...")
    write_results_to_file(regional_margins, discount_analysis, output_file)
    print(f"Results successfully written to {output_file}")
    print()

    print("=" * 60)
    print("ANALYSIS SUMMARY")
    print("=" * 60)
    print()
    print("Regional Profit Margins:")
    for region in sorted(regional_margins.keys()):
        print(f"  {region:12s}: {regional_margins[region]:6.2f}%")
    print()

    print("Discount Impact by Category:")
    for category in sorted(discount_analysis.keys()):
        data = discount_analysis[category]
        diff = data['without_discount'] - data['with_discount']
        print(f"  {category}:")
        print(f"    With Discount:    ${data['with_discount']:7.2f} (n={data['count_with_discount']})")
        print(f"    Without Discount: ${data['without_discount']:7.2f} (n={data['count_without_discount']})")
        print(f"    Difference:       ${diff:7.2f}")
        print()

    print("=" * 60)
    print("Analysis complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
