import pytest


@pytest.fixture()
def fan_type():
    """Fixture to create a TrnsysModel from xml"""
    from pyTrnsysType import TrnsysModel
    with open("tests/input_files/Type146.xml") as xml:
        fan1 = TrnsysModel.from_xml(xml.read())
    yield fan1


@pytest.fixture()
def pipe_type():
    """Fixture to create a TrnsysModel from xml"""
    from pyTrnsysType import TrnsysModel
    with open("tests/input_files/Type951.xml") as xml:
        fan1 = TrnsysModel.from_xml(xml.read())
    yield fan1


def test_cycles(pipe_type):
    n_nodes = 20
    pipe_type.parameters["Number_of_Radial_Soil_Nodes"] = n_nodes

    mylist = list(pipe_type.parameters.data.keys())
    sub = 'Radial_Distance_of_Node'
    expected = len([s for s in mylist if sub.lower() in s.lower()])

    assert n_nodes == expected


def test_cycles_2(pipe_type):
    """changing number of fluid nodes from 10 to 20 should create 20 outputs
    for pipe 2 and 20 outputs for pipe 1"""
    n_nodes = 20
    pipe_type.parameters['Number_of_Fluid_Nodes'] = n_nodes

    mylist = list(pipe_type.outputs.data.keys())
    sub_1 = 'Average_Fluid_Temperature_Pipe_1_'
    sub_2 = 'Average_Fluid_Temperature_Pipe_2_'
    expected_1 = len([s for s in mylist if sub_1.lower() in s.lower()])
    expected_2 = len([s for s in mylist if sub_2.lower() in s.lower()])

    assert n_nodes == expected_1
    assert n_nodes == expected_2


def test_out_of_bounds(pipe_type):
    """should trigger ValueError because out of bounds"""
    with pytest.raises(ValueError):
        pipe_type.parameters["Number_of_Radial_Soil_Nodes"] = 21


def test_get_attr(fan_type):
    """Test getter for class TypeVariable"""
    in_air_temp = fan_type.inputs['Inlet_Air_Temperature']
    assert in_air_temp


def test_set_attr(fan_type):
    """Test setter for class TypeVariable"""
    fan_type.inputs['Inlet_Air_Temperature'] = 12

    Q_ = fan_type.inputs['Inlet_Air_Temperature']
    assert fan_type.inputs['Inlet_Air_Temperature'] == Q_.__class__(12,
                                                                    Q_.units)
