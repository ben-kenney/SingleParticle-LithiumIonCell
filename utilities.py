import pandas
import matplotlib.pyplot as plt
import pathlib

pandas.options.mode.chained_assignment = None  # default='warn'


def returnCycleCapacity(dataFrame):
    """
    Returns a list of the discharge and charge capacities (in Ah) vs cycle number
    """
    caps = []
    for i in dataFrame.cycle.unique():
        dc = dataFrame.dCap_As[dataFrame.cycle == float(i)]
        dci = dc.index[len(dc) - 1]
        cc = dataFrame.cCap_As[dataFrame.cycle == float(i)]
        cci = cc.index[len(cc) - 1]
        caps.append([i, dc[dci] / 3600.0, cc[cci] / 3600.0])

    caps = pandas.DataFrame(caps, columns=["cycle", "dCap_Ah", "cCap_Ah"])
    return caps


def splitByCycle(dataFrame):
    """
    Split data by cycle number
    First data point of new cycle should be last data point of old cycle (to get t=0)
    """

    cycles = []
    lastTime = []

    numCycles = max(dataFrame.cycle)
    tmp = dataFrame[dataFrame.cycle == 0].reset_index()
    lastTime.append(tmp.totTime_s[tmp.index[-1]])
    cycles.append(tmp)

    for i in range(1, int(numCycles)):
        tmp1 = cycles[-1].xs(cycles[-1].index[-1])
        tmp1["totTime_s"] = tmp1["totTime_s"] + lastTime[-1]
        print(tmp1)
        tmp = dataFrame[dataFrame.cycle == i]
        lastTime.append(tmp.totTime_s[tmp.index[-1]])
        # tmp = tmp.append(tmp1,ignore_index=True)
        tmp = tmp.append(tmp1)
        tmp = tmp.sort(["totTime_s"], ascending=True)

        tmp = tmp.reset_index(drop=True)
        tmp.totTime_s = tmp.totTime_s - tmp.totTime_s[0]

        cycles.append(tmp)

    return cycles


def splitByStep(dataFrame, grab_step):
    """
    Split data by step -> grab_step could be an array

    The first data point of the step should be the last
    """

    def extract(data, step):

        if step > 0:
            tmp1 = dataFrame[dataFrame.step == step - 1]
            tmp1 = tmp1.xs(tmp1.index[-1])

        tmp = dataFrame[dataFrame.step == step]
        if step > 0:
            tmp = tmp.append(tmp1, ignore_index=True)
        tmp = tmp.sort(["totTime_s"], ascending=True)
        tmp = tmp.reset_index()
        tmp.totTime_s = tmp.totTime_s - tmp.totTime_s[0]
        return tmp

    steps = []

    try:
        num_steps = len(grab_step)
        for i in grab_step:
            steps.append(extract(dataFrame, i))

    except TypeError:
        num_steps = 1
        steps.append(extract(dataFrame, grab_step))

    return steps


def plotData(x, y):

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x, y, "-o", label="label")
    ax.set_xlabel("Time")
    ax.set_ylabel("Voltage")
    ax.set_title("Discharge")
    ax.legend()
    ax.grid()
    # plt.savefig("test.png")
    plt.show()


def main():

    data_directory = pathlib.Path().cwd() / "data"
    all_files = data_directory.glob("*.csv")

    df = pandas.concat((pandas.read_csv(f) for f in all_files), ignore_index=True)

    # capacity
    print(returnCycleCapacity(df))

    # returnCycleCapacity(data)

    # print cycle_data[3].voltage_V
    # plotData(cycle_data[3].totTime_s/3600.0,cycle_data[3].voltage_V)

    # plotData(cycle_data[1][:, 2] / 3600.0, cycle_data[1][:, 5])

    # steps = splitByStep(cycle_data[3],[0,4,8,12])
    # plotData(steps[2].totTime_s/3600.0,steps[2].voltage_V)


if __name__ == "__main__":
    main()
