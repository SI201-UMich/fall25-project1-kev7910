"""
Name: Kevin Zang
Student ID: 72328773
Email: alvinz@umich.edu
Collaborators: Worked alone.
Used AI for  function design, syntax, implementation for output txt file (especially styling), tests, etc.

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
    Writes analysis results to a text file.

    Parameters:
        regional_data (dict): Dictionary of regional profit margins
        discount_data (dict): Dictionary of discount impact analysis
        filename (str): Name of output file

    Returns:
        None (creates a file)
    """
    with open(filename, 'w') as file:
        file.write('=' * 80 + '\n')
        file.write('SUPERSTORE DATA ANALYSIS REPORT\n')
        file.write('=' * 80 + '\n\n')
        file.write('Dataset: SampleSuperstore.csv\n')
        file.write('Total Records Analyzed: 9,994\n')
        file.write('Analysis Date: 2025\n\n\n')

        file.write('=' * 80 + '\n')
        file.write('ANALYSIS 1: REGIONAL PROFITABILITY\n')
        file.write('=' * 80 + '\n\n')
        file.write('Metric: Average Profit Margin (Profit/Sales × 100)\n')
        file.write('Unit: Percentage (%)\n\n')

        sorted_regions = sorted(regional_data.items(), key=lambda x: x[1], reverse=True)

        file.write('RESULTS:\n')
        file.write('-' * 60 + '\n')
        file.write(f'{"Region":<15} {"Profit Margin":<20} {"Performance":<15}\n')
        file.write('-' * 60 + '\n')

        for region, margin in sorted_regions:
            if margin > 15:
                performance = 'Strong'
            elif margin > 0:
                performance = 'Moderate'
            else:
                performance = 'LOSS'
            file.write(f'{region:<15} {margin:>6.2f}%{"":<14} {performance:<15}\n')

        file.write('-' * 60 + '\n\n')

        best_region = sorted_regions[0]
        worst_region = sorted_regions[-1]

        file.write('KEY FINDINGS:\n')
        file.write(f'  • Best performing region: {best_region[0]} with {best_region[1]:.2f}% profit margin\n')
        file.write(f'  • Worst performing region: {worst_region[0]} with {worst_region[1]:.2f}% profit margin\n')
        file.write(f'  • Performance gap: {best_region[1] - worst_region[1]:.2f} percentage points\n')

        loss_regions = [r for r, m in regional_data.items() if m < 0]
        if loss_regions:
            file.write(f'  • ⚠️  WARNING: {", ".join(loss_regions)} region(s) operating at a loss!\n')

        file.write('\nCONCLUSION:\n')
        file.write(f'The {best_region[0]} region demonstrates the strongest profitability with a\n')
        file.write(f'{best_region[1]:.2f}% profit margin, indicating effective sales and cost management.\n')
        if loss_regions:
            file.write(f'CRITICAL: The {", ".join(loss_regions)} region requires immediate attention to\n')
            file.write(f'address negative margins and restore profitability.\n')

        file.write('\n\n')

        file.write('=' * 80 + '\n')
        file.write('ANALYSIS 2: DISCOUNT IMPACT ON PROFITABILITY\n')
        file.write('=' * 80 + '\n\n')
        file.write('Metric: Average profit per transaction\n')
        file.write('Unit: US Dollars ($)\n\n')

        file.write('RESULTS BY CATEGORY:\n\n')

        for category in sorted(discount_data.keys()):
            data = discount_data[category]
            difference = data['without_discount'] - data['with_discount']
            total_cat_orders = data['count_with_discount'] + data['count_without_discount']
            pct_with = (data['count_with_discount'] / total_cat_orders * 100)
            pct_without = (data['count_without_discount'] / total_cat_orders * 100)

            file.write(f'{category.upper()}\n')
            file.write('-' * 60 + '\n')
            file.write(f'  Orders WITH Discount:\n')
            file.write(f'    • Count: {data["count_with_discount"]:,} orders ({pct_with:.1f}% of category)\n')
            file.write(f'    • Average Profit: ${data["with_discount"]:.2f} per order\n')
            if data['with_discount'] < 0:
                file.write(f'    • ⚠️  WARNING: Operating at a LOSS!\n')

            file.write(f'\n  Orders WITHOUT Discount:\n')
            file.write(f'    • Count: {data["count_without_discount"]:,} orders ({pct_without:.1f}% of category)\n')
            file.write(f'    • Average Profit: ${data["without_discount"]:.2f} per order\n')

            file.write(f'\n  IMPACT:\n')
            file.write(f'    • Profit Reduction: ${difference:.2f} per discounted order\n')
            file.write(f'    • Total Category Orders: {total_cat_orders:,}\n\n')

        file.write('\nKEY FINDINGS:\n')

        worst_impact = max(discount_data.items(),
                          key=lambda x: x[1]['without_discount'] - x[1]['with_discount'])
        file.write(f'  • {worst_impact[0]} shows the largest profit reduction\n')
        file.write(f'    (${worst_impact[1]["without_discount"] - worst_impact[1]["with_discount"]:.2f} per discounted order)\n')

        losing_categories = [cat for cat, data in discount_data.items() if data['with_discount'] < 0]
        if losing_categories:
            file.write(f'  • ⚠️  Discounted sales in {", ".join(losing_categories)} are UNPROFITABLE\n')

        total_discount_orders = sum(d['count_with_discount'] for d in discount_data.values())
        total_orders = sum(d['count_with_discount'] + d['count_without_discount'] for d in discount_data.values())
        overall_discount_pct = (total_discount_orders / total_orders * 100)
        file.write(f'  • Overall: {overall_discount_pct:.1f}% of all orders ({total_discount_orders:,}/{total_orders:,}) received discounts\n')

        file.write('\nCONCLUSION:\n')
        file.write('Discounting significantly reduces profitability across ALL product categories.\n')
        file.write('While discounts may drive sales volume, they are severely impacting profit margins.\n')
        if losing_categories:
            file.write(f'In {", ".join(losing_categories)}, discounted orders are generating losses,\n')
            file.write('indicating the discount strategy is too aggressive for these categories.\n')

        file.write('\nRECOMMENDATION:\n')
        file.write('  1. Review and revise discount policies to preserve profit margins\n')
        file.write('  2. Consider more targeted, strategic discounting rather than broad application\n')
        file.write('  3. Set minimum profit thresholds for discounted sales\n')
        file.write(f'  4. Prioritize fixing {", ".join(losing_categories)} category discount issues immediately\n')

        file.write('\n\n')
        file.write('=' * 80 + '\n')
        file.write('END OF REPORT\n')
        file.write('=' * 80 + '\n')


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

    output_file = 'analysis_results.txt'
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
