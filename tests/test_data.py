import pytest
import pandas
import json
import re

@pytest.mark.parametrize("test_data", ["1"], indirect=True)
def test_is_file_of_type_excel(test_data):
    gtn_file, payrun_file, _ = test_data
    
    assert gtn_file.lower().endswith((".xls", ".xlsx")), "GTN file is of wrong type. It should be of type xls/xlsx"
    assert payrun_file.lower().endswith((".xls",".xlsx")), "Payrun file is of wrong type. It should be of type xls/xlsx"


@pytest.mark.parametrize("test_data", ["2"], indirect=True)
def test_gtn_has_empty_rows(test_data):
    gtn_file, _, _ = test_data

    df = pandas.read_excel(gtn_file)
    empty_rows = df.isnull().all(axis=1)

    assert not empty_rows.any(), "There are empty rows in the GTN excel file."


@pytest.mark.parametrize("test_data", ["3"], indirect=True)
def test_gtn_header_changed(test_data):
    header_structure = [
        "employee_id", "tax_id", "firstname", "lastname", "salary",
        "element1", "element2", "element3", "element4", "element5",
        "element6", "element7", "element8", "element9", "element10"
    ]
    gtn_file, _, _ = test_data

    df = pandas.read_excel(gtn_file)
    header_row = df.columns

    # Check if header is of expected structure
    assert list(header_row) == header_structure, f"Header structure is different from expected. Expected header structure is {header_structure}"

    # Regex for numeric values
    digit_pattern = r"^-?\d{1,3}(,\d{3})*(\.\d+)?$|^-?\d+(\.\d+)?$"

    # Check if first data row has numeric values (if it isn't a header)
    has_row_digits = False
    for cell in df.loc[0]:
        val = str(cell).strip()
        if val and re.match(digit_pattern, val):
            has_row_digits = True
            break

    assert has_row_digits, f"Header detected on row 2. Expected header structure is {header_structure}"



@pytest.mark.parametrize("test_data", ["4"], indirect=True)
def test_employees_in_payrun_missing_in_gtn(test_data):
    gtn_file, payrun_file, _ = test_data

    payrun_df = pandas.read_excel(payrun_file)
    gtn_df = pandas.read_excel(gtn_file)

    payrun_ids = set(payrun_df["Employee ID"].dropna().astype(int).astype(str))
    gtn_ids = set(gtn_df["employee_id"].dropna().astype(int).astype(str))

    # Check if there are employees in payrun set missing in gtn set
    missing = gtn_ids - payrun_ids

    assert len(missing) == 0, f"Employees in Payrun but missing in GTN: {missing}"


@pytest.mark.parametrize("test_data", ["5"], indirect=True)
def test_employees_in_gtn_missing_in_payrun(test_data):
    gtn_file, payrun_file, _ = test_data

    payrun_df = pandas.read_excel(payrun_file)
    gtn_df = pandas.read_excel(gtn_file)

    payrun_ids = set(payrun_df["Employee ID"].dropna().astype(int).astype(str))
    gtn_ids = set(gtn_df["employee_id"].dropna().astype(int).astype(str))

    # Check if there are employees in gtn set missing in payrun set
    missing = payrun_ids - gtn_ids

    assert len(missing) == 0, f"Employees in GTN but missing in Payrun: {missing}"


@pytest.mark.parametrize("test_data", ["6"], indirect=True)
def test_gtn_elements_have_mapping(test_data):
    gtn_file, _, mapping_file = test_data

    df = pandas.read_excel(gtn_file)
    gtn_columns = list(df.columns)
    pay_elements = gtn_columns[4:]

    with open(mapping_file, "r") as f:
        json_data = json.load(f)

    mappings = json_data["mappings"]
    not_used = json_data["not_used"]
    no_mapping = []

    for pay_element in pay_elements:
        has_mapping = False

        # First check if pay element has mapping
        for mapping in mappings.values():
            if mapping["vendor"] == pay_element and mapping["map"]:
                has_mapping = True

        # Then check if it is unused
        for unused in not_used:
            if unused["vendor"] == pay_element:
                has_mapping = True

        if not has_mapping:
            no_mapping.append(pay_element)

    assert len(no_mapping) == 0, f"The following elements have no mapping from GTN to Payrun: {no_mapping}"

@pytest.mark.parametrize("test_data", ["7"], indirect=True)
def test_payrun_elements_have_mapping(test_data):
    _, payrun_file, mapping_file = test_data

    df = pandas.read_excel(payrun_file, header=1)
    gtn_columns = list(df.columns)
    pay_elements = gtn_columns[25:37]

    with open(mapping_file, "r") as f:
        json_data = json.load(f)

    mappings = json_data["mappings"]
    no_mapping = []

    for pay_element in pay_elements:
        has_mapping = False

        # First check if pay element has mapping
        for mapping_key, mapping_value in mappings.items():
            if mapping_key == pay_element and mapping_value.get("map") and mapping_value.get("vendor"):
                has_mapping = True

        if not has_mapping:
            no_mapping.append(pay_element)

    assert len(no_mapping) == 0, f"The following elements have no mapping from Payrun to GTN: {no_mapping}"


@pytest.mark.parametrize("test_data", ["8"], indirect=True)
def test_gtn_pay_elements_have_numeric_values(test_data):
    gtn_file, _, _ = test_data

    df = pandas.read_excel(gtn_file)
    gtn_columns = list(df.columns)
    pay_elements = gtn_columns[4:]

    numeric_pattern = r"^-?\d{1,3}(,\d{3})*(\.\d+)?$|^-?\d+(\.\d+)?$"
    non_numeric_columns = {}

    for col in pay_elements:
        invalid_values = []
        for val in df[col].dropna():
            val_str = str(val).strip()
            if not re.match(numeric_pattern, val_str):
                invalid_values.append(val_str)
        if invalid_values:
            non_numeric_columns[col] = invalid_values

    assert not non_numeric_columns, f"Non-numeric values found in columns: {non_numeric_columns}"