# data-mapping-test-challenge

Contains tests on 2 datasets and a mapping file between them.
The tests are all in the ./tests/test_data.py file. 
They use conftest.py to load the correct data for each test which is stored in the ./data/data_N directory.

Description of the tests:

1. test_is_file_of_type_excel: 
    Tests both GTN and Payrun files for their format extension to be xls,xlsx (ignored case).

2. test_gtn_has_empty_rows: 
    Tests if the GTN excel file has empty rows in its dataset.

3. test_gtn_header_changed: 
    Test if the header structure in GTN file is different from expected (has more or less columns or is on multiple rows)

4. test_employees_in_payrun_missing_in_gtn: 
    Test if the Payrun file contains an Employee ID value which cannot be matched with an employee_id value in GTN.

5. test_employees_in_gtn_missing_in_payrun: 
    Same as 4. but vice versa.

6. test_gtn_elements_have_mapping: 
    Tests that mapping.json contains mapping entries for all pay elements in the GTN file. These entries should contain map=true and also should not be in ignored entries.

7. test_payrun_elements_have_mapping: 
    Tests that mapping.json contains mapping entries for all pay elements in the Payrun file. Again there must be a map=true and a vendor value.

8. test_gtn_pay_elements_have_numeric_values: 
    Matches all values in GTN with a regex for numeric values and checks if there are non-numeric values

After cloning the repository please run:
# Install requirements
pip install -r requirements.txt

# Start test
pytest ./tests/test_data.py
or
pytest

# Switch to data that passes all tests. This data is located in data/data_pass.
go to tests/conftest.py
comment out line 9
uncomment line 11
pytest ./tests/test_data.py or pytest
