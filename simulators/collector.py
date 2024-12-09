"""
A simple data collector that prints all data when the simulation finishes.

"""
import collections
import matplotlib.pyplot as plt

import mosaik_api_v3


META = {
    'type': 'event-based',
    'models': {
        'Monitor': {
            'public': True,
            'any_inputs': True,
            'params': [],
            'attrs': [],
        },
    },
}


class Collector(mosaik_api_v3.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid = None
        self.data = collections.defaultdict(lambda:
                                            collections.defaultdict(dict))

    def init(self, sid, time_resolution):
        return self.meta

    def create(self, num, model):
        if num > 1 or self.eid is not None:
            raise RuntimeError('Can only create one instance of Monitor.')

        self.eid = 'Monitor'
        return [{'eid': self.eid, 'type': model}]

    def step(self, time, inputs, max_advance):
        data = inputs.get(self.eid, {})
        for attr, values in data.items():
            for src, value in values.items():
                self.data[src][attr][time] = value

        return None

    def finalize(self):
        print('Collector in finalize. Plot data now.')

        # Initialize the plot
        plt.figure(figsize=(10, 6))

        # Iterate over each dataset in your simulation data
        for dataset_name, dataset_values in self.data.items():
            for parameter, time_series in dataset_values.items():
                times = list(time_series.keys())
                values = list(time_series.values())
                plt.plot(times, values, label=f"{dataset_name} - {parameter}")
        # Configure plot aesthetics
        plt.xlabel('Time (minutes)')
        plt.ylabel('Power (W)')
        plt.title('Simulation Data Visualization')
        plt.legend()
        plt.grid(True)

        # Display the plot
        plt.show()


if __name__ == '__main__':
    mosaik_api_v3.start_simulation(Collector())