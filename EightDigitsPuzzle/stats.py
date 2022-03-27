from matplotlib import pyplot as plt


class stats:
    def __init__(self):
        """initialize
        """        
        pass

    def draw(self, data):
        """draw stats picture, save to file

        Args:
            data (dic): information
        """
        functionName = list(data.keys())

        generatedDataList = [data['Manhattan Distance']['generationCount'],
                             data['Euclidean Distance']['generationCount'],
                             data['Cosine Distance']['generationCount']]

        expandCountList = [data['Manhattan Distance']['expandCount'],
                           data['Euclidean Distance']['expandCount'],
                           data['Cosine Distance']['expandCount']]

        timeList = [int(data['Manhattan Distance']['time']*1000),
                    int(data['Euclidean Distance']['time']*1000),
                    int(data['Cosine Distance']['time']*1000)]

        # set size
        plt.figure(figsize=(8, 6.5))
        plt.subplots_adjust(left=0.18, wspace=0.25, hspace=0.5,
                            bottom=0.05, top=0.95)

        # draw
        plt.subplot(311)
        plt.title('Generated Nodes')
        plt.bar(functionName, generatedDataList)

        plt.subplot(312)
        plt.title('Expanded Nodes')
        plt.bar(functionName, expandCountList)

        plt.subplot(313)
        plt.title('Time Used (ms)')
        plt.bar(functionName, timeList)

        # save to file
        plt.savefig('img/stats.png')
