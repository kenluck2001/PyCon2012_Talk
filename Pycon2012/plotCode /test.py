import csv
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


def prepareList(month_most_common_list):
    ''' Prepare the input for process by removing all unneccessaty values. Replace "NA" with 0'''
    output_list = []
    for x in month_most_common_list:
        if x != 'NA':
            output_list.append(x)
        else:
            output_list.append(0)
    return output_list


def plotSolarRadiationAgainstMonth(filename):
    trainRowReader = csv.reader(open(filename, 'rb'), delimiter=',')
    month_most_common_list = []
    Solar_radiation_64_list = []
    for row in trainRowReader:
        month_most_common = row[3]
        Solar_radiation_64 = row[6]
        month_most_common_list.append(month_most_common)
        Solar_radiation_64_list.append(Solar_radiation_64)   
     
    #convert all elements in the list to float while skipping the first element for the 1st element is a description of the field.
    month_most_common_list = [float(i) for i in prepareList(month_most_common_list)[1:] ]
    Solar_radiation_64_list = [float(i) for i in prepareList(Solar_radiation_64_list)[1:] ]

    fig=Figure()
    ax=fig.add_subplot(111)
    title='Scatter Diagram of solar radiation against month of the year'
    ax.set_xlabel('Most common month')
    ax.set_ylabel('Solar Radiation')
    fig.suptitle(title, fontsize=14)
    try:
        ax.scatter(month_most_common_list, Solar_radiation_64_list)
        #it is possible to make other kind of plots e.g bar charts, pie charts, histogram
    except ValueError:
        pass
    canvas = FigureCanvas(fig)
    canvas.print_figure('solarRadMonth.png',dpi=500)


if __name__ == "__main__":
    plotSolarRadiationAgainstMonth('TrainingData.csv')

