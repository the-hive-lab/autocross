# Standard library imports
import argparse

# Third party imports
import matplotlib.pyplot as plt
import numpy as np

# Local application imports
from autocross import fileio


def plot_main(args: argparse.Namespace) -> int:
    if isinstance(args.filepaths, list):
        extension = fileio.get_file_extension(args.filepaths[0])
    else:
        extension = fileio.get_file_extension(args.filepaths)

    if extension == '.cost' or extension == '.wait':
        plt.figure()

        if args.schedule is not None:
            sched_data = fileio.read_schedule_file(args.schedule)
            _, crossing_times = fileio.parse_schedule_data(sched_data)

        for index, file in enumerate(args.filepaths):
            filename = fileio.get_file_name(file)
            cost_data = fileio.read_cost_file(file)
            cost_func, cost_bounds = fileio.parse_cost_data(cost_data)

            times = np.arange(start=cost_bounds[0], stop=cost_bounds[1],
                              step=0.1)

            plt.plot(times, cost_func(times), label=filename)

            from pathlib import Path
            out_path = Path(args.filepaths[0])
            out_data = [[time, cost] for time, cost in zip(times, np.squeeze(np.asarray(cost_func(times), dtype=object)))]
            np.savetxt(f'{out_path.name}.dat', out_data, header='time cost', comments='')

            if args.schedule is not None:
                plt.plot(crossing_times[index],
                         cost_func(crossing_times[index]),
                         marker='o',
                         color='red')

        plt.title(f'{extension[1:]}')
        plt.legend()
        plt.show()
    elif extension == '.system':
        data = fileio.read_system_file(args.filepaths[0])
        states, inputs = fileio.parse_system_data(data)

        for index, state in enumerate(states):
            plt.plot(state, label=f'{index}')
        plt.title('states')
        plt.legend()
        plt.show()

        for index, input_ in enumerate(inputs):
            plt.plot(input_, label=f'{index}')
        plt.title('inputs')
        plt.legend()
        plt.show()

        ref = data['ref']
        plt.plot(ref[1], ref[0])
        plt.plot(states[1], states[0])
        plt.title('x-y')
        plt.xlabel('y')
        plt.xlim(max(states[1]), min(states[1]))
        plt.ylabel('x')
        plt.legend(['ref', 'act'])
        plt.show()

    return 0
