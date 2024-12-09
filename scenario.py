"""
Simulation scenario implemented in mosaik for seminar "Smart Grid Research".
"""

"""
Add Python imports.
"""

import mosaik.util

"""
Define how to start the adapter.
"""
SIM_CONFIGURATION = {
    'CSV': {
        'python': 'mosaik_csv:CSV',
    },
    'PV': {
        'python': 'mosaik_components.pv.pvsimulator:PVSimulator'
    },
    'Collector': {
        'python': 'simulators.collector:Collector'
    }
}

# define basic constants such as the duration of the simulation
START = '2014-01-01 00:00:00'
SIMULATION_END = 24 * 3600  # 1 day

"""
Start simulator processes. 
"""

world = mosaik.World(SIM_CONFIGURATION)

# PV
PV_DATA = 'csv_data/pv_10kw.csv'
SIM_START = '2014-01-01 00:00:00'
pv_data = world.start("CSV",
                      sim_start=SIM_START,
                      datafile=PV_DATA)

# Household
HH_DATA = 'csv_data/household_load_profile.csv'
household_data_simulator = world.start("CSV",
                                       sim_start=SIM_START,
                                       datafile=HH_DATA)

"""
Instantiate model entities and parametrize. 
"""

pv_data_model = pv_data.PV()

hh_data_model = household_data_simulator.Household()

collector = world.start('Collector')
monitor = collector.Monitor()

"""
Connect models via dataflow. 
"""
world.connect(pv_data_model, monitor, 'P[W]')
world.connect(hh_data_model, monitor, 'P[W]')

"""
Start the simulation.
"""
world.run(until=SIMULATION_END)
