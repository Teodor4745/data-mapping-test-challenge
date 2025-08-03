import os
import pytest

# Module to manage getting the correct data for each test with the parameter test_number
@pytest.fixture
def test_data(request):
    test_number = request.param

    data_dir = os.path.join(os.path.dirname(__file__), "..", "data", f"data_{test_number}")
    # Data that will pass all tests
    #data_dir = os.path.join(os.path.dirname(__file__), "..", "data", f"data_pass")

    gtn_file = ""
    payrun_file = ""
    mapping_file = ""
    for file in os.listdir(data_dir):
        full_path = os.path.join(data_dir, file)
        if file.startswith("GTN"):
            gtn_file = full_path
        elif file.startswith("Payrun"):
            payrun_file = full_path
        elif file.startswith("mapping"):
            mapping_file = full_path
    return gtn_file, payrun_file, mapping_file